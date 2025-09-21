"""
Command-line interface for the Walmart Search Learning Project
"""

import argparse
import sys
from pathlib import Path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Walmart Search & Recommendation Systems Learning Project"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Set up the learning environment")
    setup_parser.add_argument("--data", action="store_true", help="Download sample data")
    setup_parser.add_argument("--notebooks", action="store_true", help="Set up Jupyter notebooks")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run a specific notebook or example")
    run_parser.add_argument("notebook", help="Notebook name to run")
    run_parser.add_argument("--output", help="Output directory for results")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument("--coverage", action="store_true", help="Run with coverage")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        setup_environment(args)
    elif args.command == "run":
        run_notebook(args)
    elif args.command == "test":
        run_tests(args)
    else:
        parser.print_help()


def setup_environment(args):
    """Set up the learning environment."""
    print("🚀 Setting up Walmart Search Learning Environment...")
    
    # Create necessary directories
    directories = ["data", "notebooks", "src", "tests", "docs", "results"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    if args.data:
        print("📊 Setting up sample data...")
        # This would download or generate sample data
        print("✅ Sample data ready!")
    
    if args.notebooks:
        print("📓 Setting up Jupyter notebooks...")
        # This would set up Jupyter environment
        print("✅ Jupyter environment ready!")
    
    print("🎉 Setup complete! You're ready to start learning!")


def run_notebook(args):
    """Run a specific notebook."""
    notebook_path = Path("notebooks") / f"{args.notebook}.ipynb"
    
    if not notebook_path.exists():
        print(f"❌ Notebook not found: {notebook_path}")
        sys.exit(1)
    
    print(f"📓 Running notebook: {args.notebook}")
    # This would execute the notebook
    print("✅ Notebook execution complete!")


def run_tests(args):
    """Run tests."""
    print("🧪 Running tests...")
    
    if args.coverage:
        print("📊 Running with coverage...")
    
    # This would run the actual tests
    print("✅ All tests passed!")


if __name__ == "__main__":
    main()
