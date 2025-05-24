# External Merge Sort Implementation

![Sorting Visualization]<!-- Replace with actual visualization -->

An efficient external merge sort implementation for large datasets that exceed available memory, featuring web-based monitoring and MongoDB integration.

## Key Features

- **Memory-Efficient Sorting**: Handles datasets larger than available RAM
- **Web Interface**: Real-time progress monitoring and visualization
- **MongoDB Integration**: Stores and retrieves sorted results
- **Performance Metrics**: Detailed timing breakdowns for each processing phase

## Performance Metrics

| Phase                     | Time Range       |
|---------------------------|------------------|
| Data Generation           | 0.5-1.0 seconds  |
| Individual File Sorting    | 0.1-0.3 seconds |
| K-way Merge Phase         | 0.2-0.5 seconds |
| **Total Processing Time** | **1.0-2.0 seconds** |

## Advanced Features

### Memory Management
- Configurable chunk sizes for different memory constraints
- Automatic cleanup of temporary files
- Efficient file handling with proper resource management

### Error Handling
- Comprehensive exception handling
- User-friendly error messages in web interface
- Database connection resilience

### Scalability
- Modular design for larger datasets
- Configurable parameters for different hardware
- Efficient MongoDB indexing for fast queries

## Installation

```bash
git clone https://github.com/yourusername/external-merge-sort.git
cd external-merge-sort
pip install -r requirements.txt
