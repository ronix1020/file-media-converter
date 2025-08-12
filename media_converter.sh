#!/bin/bash

echo "PTAV Media File Converter"
echo "========================"
echo

# Check if Python script exists
if [ ! -f "ptav_analyzer.py" ]; then
    echo "Error: ptav_analyzer.py not found!"
    echo "Please ensure the PTAV analyzer script is in the same directory."
    exit 1
fi

# Clean up any previous conversion files
echo "Cleaning up previous conversion files..."
rm -f *_converted.mp4 converted_files.txt final_output.mp4

# Count .media files
media_count=$(find . -name '*.media' | wc -l)
if [ $media_count -eq 0 ]; then
    echo "No .media files found in current directory!"
    exit 1
fi

echo "Found $media_count .media files"
echo

# Convert all PTAV files to MP4
echo "Converting PTAV files to MP4..."
if python3 ptav_analyzer.py; then
    echo
    echo "Conversion completed!"
else
    echo "Error during conversion process"
    exit 1
fi

# Check if we have any converted files
converted_count=$(find . -name '*_converted.mp4' | wc -l)
if [ $converted_count -eq 0 ]; then
    echo "No files were successfully converted."
    echo "The .media files may be in an unsupported variant of the PTAV format."
    exit 1
fi

echo "Successfully converted $converted_count out of $media_count files"
echo

# Concatenate all converted files if we have more than one
if [ $converted_count -gt 1 ]; then
    echo "Concatenating all converted files into final_output.mp4..."
    if [ -f "converted_files.txt" ]; then
        if ffmpeg -y -f concat -safe 0 -i converted_files.txt -c copy final_output.mp4; then
            echo "Success! Final video saved as final_output.mp4"
            
            # Get info about final video
            echo
            echo "Final video information:"
            ffprobe -v quiet -select_streams v:0 -show_entries stream=codec_name,width,height,duration -of csv=p=0 final_output.mp4 | while IFS=, read codec width height duration; do
                echo "  Codec: $codec"
                echo "  Resolution: ${width}x${height}"
                echo "  Duration: $duration seconds"
            done
            
            # Offer to clean up intermediate files
            echo
            read -p "Delete intermediate converted files? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                rm -f *_converted.mp4 converted_files.txt
                echo "Intermediate files deleted."
            fi
        else
            echo "Failed to concatenate files. Individual converted files are available."
        fi
    else
        echo "Error: converted_files.txt not found"
    fi
elif [ $converted_count -eq 1 ]; then
    # Only one file, just rename it
    converted_file=$(find . -name '*_converted.mp4' | head -n 1)
    mv "$converted_file" final_output.mp4
    echo "Single file converted and renamed to final_output.mp4"
fi

echo
echo "Processing complete!"
