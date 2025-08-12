# PTAV Media File Converter

A complete solution for converting proprietary PTAV (`.media`) files from security cameras and surveillance systems to standard MP4 format.

## Overview

This toolkit addresses the common "Invalid data found when processing input" error that occurs when trying to process `.media` files with FFmpeg directly. The PTAV format is a proprietary video container format used by various security camera systems that wraps standard H.264 video streams in a custom header structure.

## Features

- ✅ **Automatic PTAV format detection and analysis**
- ✅ **H.264 stream extraction from proprietary containers**
- ✅ **Batch conversion of multiple files**
- ✅ **Automatic concatenation of converted videos**
- ✅ **Progress reporting and error handling**
- ✅ **Quality preservation (no re-encoding)**
- ✅ **Cross-platform compatibility**

## Files Included

- `media_converter.sh` - Main conversion script with user-friendly interface
- `ptav_analyzer.py` - Core Python script for PTAV analysis and conversion
- `README.md` - This documentation file

## Requirements

### System Requirements
- **macOS, Linux, or Windows** (with appropriate shell)
- **Python 3.6+**
- **FFmpeg** (installed and available in PATH)

### Dependencies
- Python 3 standard library (no additional packages required)
- FFmpeg with H.264 support

### Installation Check
Verify your system has the required components:
```bash
# Check Python version
python3 --version

# Check FFmpeg installation
ffmpeg -version

# Make scripts executable (macOS/Linux)
chmod +x media_converter.sh
chmod +x ptav_analyzer.py
```

## Quick Start

### Convert All .media Files (Recommended)
```bash
./media_converter.sh
```

This single command will:
1. Find all `.media` files in the current directory
2. Convert each file to MP4 format
3. Concatenate all converted files into `final_output.mp4`
4. Show progress and provide feedback

### Example Output
```
PTAV Media File Converter
========================

Found 200 .media files

Converting PTAV files to MP4...
Processing file 1/200: 20220708154051.media
  PTAV Version: 1
  Found 4 potential H.264 NAL markers
  Successfully converted to: 20220708154051_converted.mp4
...

Successfully converted 200 out of 200 files

Concatenating all converted files into final_output.mp4...
Success! Final video saved as final_output.mp4

Final video information:
  Codec: h264
  Resolution: 2304x1296
  Duration: 6458.100000 seconds
```

## Advanced Usage

### Convert Specific Files
```bash
python3 ptav_analyzer.py file1.media file2.media file3.media
```

### Manual Step-by-Step Process
```bash
# 1. Convert all files
python3 ptav_analyzer.py

# 2. Manually concatenate (if needed)
ffmpeg -f concat -safe 0 -i converted_files.txt -c copy final_output.mp4
```

### Process Files in Different Directory
```bash
# Navigate to the directory containing .media files
cd /path/to/media/files

# Run the converter
/path/to/media_converter.sh
```

## Technical Details

### PTAV Format Structure
The PTAV format consists of:
- **Header**: 4-byte signature "PTAV"
- **Version**: 4-byte little-endian integer
- **Metadata**: Width, height, and other parameters
- **Video Data**: Raw H.264 stream starting at byte offset 29

### Conversion Process
1. **Header Analysis**: Reads and parses the PTAV header structure
2. **Stream Detection**: Locates H.264 NAL unit markers (0x00000001)
3. **Data Extraction**: Extracts raw H.264 data from offset 29 onwards
4. **Container Wrapping**: Uses FFmpeg to wrap H.264 stream in MP4 container
5. **Quality Preservation**: No re-encoding ensures original quality

### Output Specifications
- **Format**: MP4 (H.264 video)
- **Quality**: Original quality preserved
- **Naming**: `[original_name]_converted.mp4`
- **Final Output**: `final_output.mp4` (concatenated result)

## File Structure After Conversion

```
your-directory/
├── 20220708154051.media          # Original PTAV file
├── 20220708154051_converted.mp4  # Converted MP4 file
├── 20220708154307.media
├── 20220708154307_converted.mp4
├── ...
├── converted_files.txt           # List for concatenation
├── final_output.mp4             # Final concatenated video
├── media_converter.sh           # Main script
├── ptav_analyzer.py            # Core converter
└── README.md                   # This documentation
```

## Troubleshooting

### Common Issues

#### "Permission denied" Error
```bash
# Make scripts executable
chmod +x media_converter.sh
chmod +x ptav_analyzer.py
```

#### "FFmpeg not found" Error
```bash
# Install FFmpeg (macOS with Homebrew)
brew install ffmpeg

# Install FFmpeg (Ubuntu/Debian)
sudo apt update && sudo apt install ffmpeg

# Install FFmpeg (Windows)
# Download from https://ffmpeg.org/download.html
```

#### "No .media files found"
- Ensure you're in the correct directory containing `.media` files
- Check file permissions and accessibility
- Verify files have the correct `.media` extension

#### Conversion Failures
- **File Corruption**: Some `.media` files may be corrupted or incomplete
- **Format Variations**: Different camera manufacturers may use slightly different PTAV implementations
- **Partial Conversion**: Script will continue with remaining files if some fail

### Error Messages

| Error | Cause | Solution |
|-------|--------|----------|
| `Invalid data found when processing input` | Original FFmpeg limitation with PTAV format | Use this converter toolkit |
| `No H.264 stream found` | File may be corrupted or use different codec | Check file integrity |
| `FFmpeg conversion failed` | Invalid H.264 data extracted | File may be damaged |
| `sps_id 32 out of range` | Normal FFmpeg warning during concatenation | Safe to ignore |

## Performance

### Conversion Speed
- **Extraction**: Very fast (data copying only)
- **Container Wrapping**: Fast (no re-encoding)
- **Concatenation**: Moderate (depends on total file size)

### Storage Requirements
- **Temporary Space**: ~2x original file size during conversion
- **Final Space**: Slightly larger than original (MP4 container overhead)
- **Cleanup**: Intermediate files can be safely deleted

## Supported Formats

### Input Formats
- ✅ **PTAV v1** (tested and verified)
- ✅ **H.264 video streams** within PTAV containers
- ❓ **Other PTAV versions** (may work but untested)

### Output Formats
- ✅ **MP4** (H.264 video)
- ✅ **Standard video players** (VLC, QuickTime, etc.)
- ✅ **Video editing software** compatibility
- ✅ **Web browser** playback support

## Security and Privacy

- **Local Processing**: All conversion happens locally on your machine
- **No Network Access**: Scripts don't send data anywhere
- **Original Files**: Preserved unchanged during conversion
- **Temporary Files**: Automatically cleaned up

## Contributing

Found a bug or have a suggestion? This toolkit was created to solve the specific PTAV format challenge. For improvements:

1. Test with your specific camera model
2. Report any format variations encountered
3. Share successful camera compatibility information

## License

This toolkit is provided as-is for educational and personal use. Use responsibly and ensure you have proper rights to convert the media files.

## Version History

- **v1.0**: Initial release with PTAV v1 support
- **Current**: Enhanced error handling and progress reporting

## Camera Compatibility

Tested with PTAV files from various security camera systems:
- ✅ **Generic PTAV v1** format
- ✅ **2304x1296 resolution** files
- ✅ **H.264 video streams**

## Technical Support

### Common Success Patterns
- Files with consistent PTAV headers
- H.264 streams starting at offset 29
- Sequential timestamp naming
- Consistent resolution and format

### System Information
When reporting issues, include:
- Operating system and version
- Python version (`python3 --version`)
- FFmpeg version (`ffmpeg -version`)
- Sample file size and naming pattern
- Error messages (full output)

---

**Note**: This toolkit specifically addresses the proprietary PTAV format used by security cameras. If you're working with different formats or encountering different errors, you may need alternative solutions.
