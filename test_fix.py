"""Quick Test Script - Verify Polyhedra is Working"""

import sys
from pathlib import Path

def test_imports():
    """Test basic imports"""
    print("🔍 Test 1: Check imports...")
    try:
        from polyhedra.services.semantic_scholar import SemanticScholarService
        from polyhedra.services.citation_manager import CitationManager
        from polyhedra.services.context_manager import ContextManager
        from polyhedra.services.rag_service import RAGService
        from polyhedra.services.project_initializer import ProjectInitializer
        print("✅ All service modules imported successfully\n")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}\n")
        return False

def test_service_creation():
    """Test service instantiation"""
    print("🔍 Test 2: Create service instance...")
    try:
        from polyhedra.services.semantic_scholar import SemanticScholarService
        _ = SemanticScholarService()  # Create instance to verify it works
        print("✅ SemanticScholarService created successfully\n")
        return True
    except Exception as e:
        print(f"❌ Service creation failed: {e}\n")
        return False

def test_server_module():
    """Test server module loading (without starting)"""
    print("🔍 Test 3: Check server module...")
    try:
        # Only import functions, don't execute
        from polyhedra.server import get_services, get_project_root
        root = get_project_root()
        print(f"✅ Server module OK, project root: {root}\n")
        return True
    except Exception as e:
        print(f"❌ Server module loading failed: {e}\n")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 Polyhedra Quick Diagnostic Test")
    print("="*60 + "\n")
    
    results = []
    
    # Run tests
    results.append(("Import Test", test_imports()))
    results.append(("Service Creation", test_service_creation()))
    results.append(("Server Module", test_server_module()))
    
    # Summarize results
    print("="*60)
    print("📊 Test Results Summary:")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ Passed" if result else "❌ Failed"
        print(f"  {name:20} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Polyhedra basic functionality is working.")
        print("\nNext steps:")
        print("  1. Reload VS Code (Ctrl+Shift+P -> 'Reload Window')")
        print("  2. Test in AI chat: 'Search for transformer papers'")
        print("  3. Run full demo: python demo_search.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check:")
        print("  1. Is virtual environment activated?")
        print("  2. Are dependencies fully installed: pip install -e .")
        print("  3. Is Python version >= 3.11?")
        return 1

if __name__ == "__main__":
    sys.exit(main())
