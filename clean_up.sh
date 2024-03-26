
# Path to your .tex file
TEX_FILE="neurips_Diffusion_Geometry.tex"

# Directory containing the files to check
DIR="figs"

# Temporary file to store references from .tex file
REFERENCES=$(mktemp)

# Extract references, accounting for the escaping issue
grep -o '\\includegraphics{[^}]*}' "$TEX_FILE" | sed 's/\\includegraphics{\(.*\)}/\1/' > "$REFERENCES"

# Find all files in the directory (and subdirectories)
find "$DIR" -type f | while read -r file; do
    # Extract just the filename without path
    filename=$(basename "$file")
    
    # Check if the filename is mentioned in the .tex references
    if ! grep -Fq "$filename" "$REFERENCES"; then
        # If not, print the file path
        echo "$file is not linked in the .tex file."
        rm $file
    fi
done

# Clean up
rm "$REFERENCES"