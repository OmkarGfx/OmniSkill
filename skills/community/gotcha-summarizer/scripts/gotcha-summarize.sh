#!/bin/bash
# Gotcha Summarizer Wrapper Script
# Automatically summarizes technical lessons from Claude Code conversations

set -e

# Default values
DRY_RUN=false
GOTCHAS_DIR="${GOTCHAS_DIR:-./docs/gotchas}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --gotchas-dir)
            GOTCHAS_DIR="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: gotcha-summarize.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --dry-run       Preview changes without writing files"
            echo "  --gotchas-dir   Path to docs/gotchas directory (default: ./docs/gotchas)"
            echo "  -h, --help      Show this help message"
            echo ""
            echo "Environment Variables:"
            echo "  GOTCHAS_DIR       Path to docs/gotchas directory"
            echo "  DRY_RUN          Set to 'true' for dry run mode"
            echo "  CLAUDE_HISTORY_PATH  Path to conversation history file"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Run the Python script
if [ "$DRY_RUN" = true ]; then
    python3 "$SCRIPT_DIR/summarize.py" --dry-run --gotchas-dir "$GOTCHAS_DIR"
else
    python3 "$SCRIPT_DIR/summarize.py" --gotchas-dir "$GOTCHAS_DIR"
fi
