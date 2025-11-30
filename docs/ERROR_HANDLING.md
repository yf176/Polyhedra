# Error Handling Guide

This document describes how Polyhedra handles errors and provides guidance for error recovery.

## Error Categories

### 1. Network Errors

**API Connection Failures:**
```
Error: "Semantic Scholar API error: 503 - Service temporarily unavailable"
Recovery: Wait a few minutes and retry the search
```

**Rate Limiting:**
```
Error: "Failed after 3 retries due to rate limiting"
Recovery: Wait 60 seconds before making another request
Note: Polyhedra automatically retries with exponential backoff
```

**Timeout:**
```
Error: "HTTP error occurred: Timeout"
Recovery: Check internet connection and retry
```

**DNS Failure:**
```
Error: "HTTP error occurred: DNSError"
Recovery: Check network connectivity
```

### 2. File System Errors

**Permission Denied:**
```
Error: "Permission denied: /path/to/file"
Recovery: Check file/directory permissions
```

**File Not Found:**
```
Response: {"contents": {}, "missing": ["file.md"]}
Recovery: Check file path spelling and existence
Note: Missing files are reported but don't cause failures
```

**Directory Creation Failed:**
```
Error: "Cannot create directory: Permission denied"
Recovery: Check parent directory permissions or use different location
```

### 3. Validation Errors

**Invalid BibTeX Format:**
```
Error: "Invalid BibTeX format: Expected @ symbol"
Recovery: Validate BibTeX syntax using online validator
```

**Missing Required Fields:**
```
Error: "BibTeX entry missing required ID field"
Recovery: Ensure BibTeX entry has proper citation key
```

**Empty Input:**
```
Error: "Query cannot be empty"
Recovery: Provide a non-empty search query
```

**Invalid Parameters:**
```
Error: "Limit must be between 1 and 100"
Recovery: Adjust parameter to valid range
```

**Missing Title in Paper:**
```
Error: "Paper missing required 'title' field"
Recovery: Ensure papers.json entries have title field
```

### 4. State Errors

**RAG Not Indexed:**
```
Error: "Papers not indexed. Run index_papers first."
Recovery: Run index_papers tool before querying
```

**Papers File Missing:**
```
Error: "Papers file not found: literature/papers.json"
Recovery: Create literature/papers.json or specify correct path
```

**Empty Papers List:**
```
Error: "Cannot index empty papers list"
Recovery: Add papers to papers.json before indexing
```

## Error Response Format

All errors are returned in consistent JSON format:

```json
{
  "error": "Description of what went wrong",
  "tool": "tool_name",
  "details": "Additional context (optional)"
}
```

## Graceful Degradation

### Multiple File Operations

When reading multiple files, Polyhedra processes all valid files and reports missing ones:

```json
{
  "contents": {
    "file1.md": "content of file 1",
    "file2.md": "content of file 2"
  },
  "missing": ["file3.md", "file4.md"]
}
```

### Partial Citation Processing

When adding multiple citations:
- Valid citations are added
- Invalid citations are reported
- Process continues for remaining citations

### Paper Search with Filters

If no papers match filters:
```json
[]
```
Empty array indicates no matches (not an error)

## Retry Strategy

### Automatic Retries

Polyhedra automatically retries network operations:

**Configuration:**
- Max retries: 3
- Retry delay: 1 second (first), 2 seconds (second), 4 seconds (third)
- Only retries on: 429 (rate limit), timeouts, connection errors

**Not Retried:**
- 400 Bad Request (client error)
- 401 Unauthorized
- 404 Not Found
- Validation errors

### Manual Retry Guidance

For user-level retries:

1. **Rate Limiting**: Wait 60 seconds
2. **Network Issues**: Check connectivity, retry immediately
3. **Service Unavailable**: Wait 5-10 minutes
4. **Validation Errors**: Fix input, retry immediately

## Error Prevention

### Best Practices

1. **Before Querying Similar Papers:**
   - Run `index_papers` first
   - Verify papers.json exists

2. **Before Adding Citations:**
   - Validate BibTeX format
   - Ensure citation key is unique

3. **Before Writing Files:**
   - Check parent directory exists
   - Verify write permissions

4. **For Paper Searches:**
   - Keep queries specific but not too narrow
   - Use reasonable limits (10-50)
   - Apply year filters to reduce results

## Debugging Errors

### Enable Verbose Logging

Set environment variable:
```bash
export POLYHEDRA_LOG_LEVEL=DEBUG
```

### Common Issues and Solutions

**"No tools available in IDE"**
- Check MCP configuration file location
- Restart IDE completely
- Verify Polyhedra is installed: `pip list | grep polyhedra`

**"Tool execution failed"**
- Check you're in a valid project directory
- Verify required files exist (papers.json, references.bib)
- Check file permissions

**"Connection timeout"**
- Check internet connectivity
- Verify Semantic Scholar API is accessible
- Try with VPN if behind firewall

**"Invalid BibTeX"**
- Use online BibTeX validator
- Check for missing commas, braces
- Ensure citation key follows format

## Error Logging

### Log Locations

**Development:**
- Console output (stderr)

**Production:**
- System logs (varies by OS)
- IDE error console

### Log Levels

- **ERROR**: Critical failures requiring attention
- **WARNING**: Issues that don't prevent operation
- **INFO**: Normal operation messages
- **DEBUG**: Detailed troubleshooting information

## Error Recovery Examples

### Example 1: Handle Missing Files

```python
# IDE Chat Request
"Read files: paper/intro.md, paper/method.md, missing.md"

# Response
{
  "contents": {
    "paper/intro.md": "# Introduction...",
    "paper/method.md": "# Method..."
  },
  "missing": ["missing.md"]
}

# Recovery Action
Create missing.md or continue with available files
```

### Example 2: Rate Limit Recovery

```python
# First request succeeds
search_papers("machine learning", limit=10)

# Second request hits rate limit
Error: "Failed after 3 retries due to rate limiting"

# Recovery
Wait 60 seconds
Retry search_papers("deep learning", limit=5)
Success!
```

### Example 3: Invalid Citation Recovery

```python
# Attempt to add invalid BibTeX
add_citation("@article invalid")

# Response
{
  "error": "Invalid BibTeX format: Expected '{'",
  "tool": "add_citation"
}

# Recovery
# Fix BibTeX format
add_citation("@article{key2021, title={Test}, year={2021}}")

# Success!
{
  "key": "key2021",
  "added": true,
  "message": "Citation 'key2021' added"
}
```

## Support

For unresolved errors:

1. Check this guide for similar issues
2. Review logs for detailed error messages
3. Consult API documentation for service-specific errors
4. Report bugs: https://github.com/polyhedra/polyhedra/issues
