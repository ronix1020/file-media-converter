#!/usr/bin/env python3
"""
PTAV Media File Analyzer and Converter
Analyzes .media files with PTAV headers and attempts to extract/convert video streams
"""

import os
import struct
import sys
from pathlib import Path

def analyze_ptav_header(filepath):
    """Analyze the PTAV header structure"""
    try:
        with open(filepath, 'rb') as f:
            # Read first 64 bytes to analyze header
            header = f.read(64)
            
            if len(header) < 16:
                return None
                
            # Check for PTAV signature
            if header[:4] != b'PTAV':
                return None
                
            # Parse basic header structure
            version = struct.unpack('<I', header[4:8])[0]
            data1 = struct.unpack('<I', header[8:12])[0]
            data2 = struct.unpack('<I', header[12:16])[0]
            
            print(f"File: {filepath}")
            print(f"  PTAV Version: {version}")
            print(f"  Data1: {data1} (0x{data1:08x})")
            print(f"  Data2: {data2} (0x{data2:08x})")
            
            # Look for potential video stream markers
            # Check for common video codec signatures in the data
            file_size = os.path.getsize(filepath)
            f.seek(0)
            data = f.read(min(1024, file_size))  # Read first 1KB
            
            # Look for H.264 NAL unit markers (0x00000001)
            h264_markers = []
            for i in range(len(data) - 4):
                if data[i:i+4] == b'\x00\x00\x00\x01':
                    h264_markers.append(i)
            
            if h264_markers:
                print(f"  Found {len(h264_markers)} potential H.264 NAL markers")
                print(f"  First marker at offset: {h264_markers[0]}")
                
                # Try to extract from first H.264 marker
                return {
                    'format': 'PTAV',
                    'version': version,
                    'h264_offset': h264_markers[0],
                    'file_size': file_size
                }
            
            return {
                'format': 'PTAV',
                'version': version,
                'file_size': file_size
            }
            
    except Exception as e:
        print(f"Error analyzing {filepath}: {e}")
        return None

def extract_video_stream(filepath, info):
    """Attempt to extract video stream from PTAV file"""
    if 'h264_offset' not in info:
        print(f"No H.264 stream found in {filepath}")
        return False
        
    try:
        output_path = filepath.replace('.media', '_extracted.h264')
        
        with open(filepath, 'rb') as infile, open(output_path, 'wb') as outfile:
            # Skip to H.264 data
            infile.seek(info['h264_offset'])
            
            # Copy remaining data
            chunk_size = 64 * 1024  # 64KB chunks
            while True:
                chunk = infile.read(chunk_size)
                if not chunk:
                    break
                outfile.write(chunk)
                
        print(f"Extracted H.264 stream to: {output_path}")
        
        # Try to convert with ffmpeg
        import subprocess
        mp4_output = filepath.replace('.media', '_converted.mp4')
        
        cmd = [
            'ffmpeg', '-y',
            '-i', output_path,
            '-c:v', 'copy',  # Copy without re-encoding
            '-f', 'mp4',
            mp4_output
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Successfully converted to: {mp4_output}")
            # Clean up intermediate file
            os.remove(output_path)
            return True
        else:
            print(f"FFmpeg conversion failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error extracting from {filepath}: {e}")
        return False

def main():
    if len(sys.argv) > 1:
        media_files = sys.argv[1:]
    else:
        # Find all .media files in current directory
        media_files = list(Path('.').glob('*.media'))
    
    if not media_files:
        print("No .media files found")
        return
    
    print(f"Found {len(media_files)} .media files")
    print("=" * 50)
    
    successful_conversions = 0
    
    for i, media_file in enumerate(sorted(media_files), 1):
        print(f"Processing file {i}/{len(media_files)}: {media_file}")
        info = analyze_ptav_header(str(media_file))
        
        if info:
            if extract_video_stream(str(media_file), info):
                successful_conversions += 1
        
        print("-" * 50)
    
    print(f"\nSummary: {successful_conversions}/{len(media_files)} files successfully converted")
    
    if successful_conversions > 0:
        # Create a list of converted files for concatenation
        converted_files = list(Path('.').glob('*_converted.mp4'))
        if converted_files:
            print("\nCreating file list for concatenation...")
            with open('converted_files.txt', 'w') as f:
                for file in sorted(converted_files):
                    f.write(f"file '{file}'\n")
            
            print("To concatenate all converted files, run:")
            print("ffmpeg -f concat -safe 0 -i converted_files.txt -c copy final_output.mp4")

if __name__ == '__main__':
    main()
