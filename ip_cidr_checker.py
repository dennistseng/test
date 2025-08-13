#!/usr/bin/env python3
"""
Script to check if IP addresses fall within CIDR ranges.
"""

import ipaddress
from typing import List, Dict, Set

def check_ip_in_cidr_ranges(ip_addresses: List[str], cidr_ranges: List[str]) -> Dict[str, List[str]]:
    """
    Check which CIDR ranges each IP address falls into.
    
    Args:
        ip_addresses: List of IP addresses to check
        cidr_ranges: List of CIDR ranges to check against
    
    Returns:
        Dictionary mapping each IP address to list of matching CIDR ranges
    """
    results = {}
    
    # Parse CIDR ranges once
    parsed_cidrs = []
    for cidr in cidr_ranges:
        try:
            parsed_cidrs.append((cidr, ipaddress.ip_network(cidr, strict=False)))
        except ValueError as e:
            print(f"Warning: Invalid CIDR range '{cidr}': {e}")
            continue
    
    # Check each IP address
    for ip_str in ip_addresses:
        try:
            ip = ipaddress.ip_address(ip_str)
            matching_ranges = []
            
            for cidr_str, cidr_network in parsed_cidrs:
                if ip in cidr_network:
                    matching_ranges.append(cidr_str)
            
            results[ip_str] = matching_ranges
            
        except ValueError as e:
            print(f"Warning: Invalid IP address '{ip_str}': {e}")
            results[ip_str] = []
    
    return results

def find_unmatched_ips(results: Dict[str, List[str]]) -> List[str]:
    """Find IP addresses that don't match any CIDR range."""
    return [ip for ip, ranges in results.items() if not ranges]

def print_results(results: Dict[str, List[str]], show_all: bool = True):
    """Print the results in a readable format."""
    print("\n" + "="*60)
    print("IP ADDRESS CIDR RANGE CHECK RESULTS")
    print("="*60)
    
    for ip, ranges in results.items():
        if ranges:
            print(f"\n✓ {ip}")
            for range_str in ranges:
                print(f"  └─ Matches: {range_str}")
        elif show_all:
            print(f"\n✗ {ip}")
            print("  └─ No matches found")
    
    # Summary
    matched_count = sum(1 for ranges in results.values() if ranges)
    total_count = len(results)
    
    print(f"\n" + "-"*40)
    print(f"SUMMARY:")
    print(f"Total IPs checked: {total_count}")
    print(f"IPs with matches: {matched_count}")
    print(f"IPs without matches: {total_count - matched_count}")

def main():
    # Example data - replace with your actual lists
    cidr_ranges = [
        "192.168.1.0/24",
        "10.0.0.0/8", 
        "172.16.0.0/12",
        "203.0.113.0/24",
        "2001:db8::/32"  # IPv6 example
    ]
    
    ip_addresses = [
        "192.168.1.10",
        "192.168.1.255", 
        "10.0.0.1",
        "10.255.255.255",
        "172.16.0.1",
        "172.20.1.1",
        "8.8.8.8",
        "203.0.113.50",
        "2001:db8::1"  # IPv6 example
    ]
    
    print("CIDR Ranges to check against:")
    for cidr in cidr_ranges:
        print(f"  - {cidr}")
    
    print(f"\nIP Addresses to check:")
    for ip in ip_addresses:
        print(f"  - {ip}")
    
    # Perform the check
    results = check_ip_in_cidr_ranges(ip_addresses, cidr_ranges)
    
    # Display results
    print_results(results)
    
    # Find unmatched IPs
    unmatched = find_unmatched_ips(results)
    if unmatched:
        print(f"\nUnmatched IP addresses:")
        for ip in unmatched:
            print(f"  - {ip}")

# Additional utility functions for different use cases

def load_ips_from_file(filename: str) -> List[str]:
    """Load IP addresses from a text file (one per line)."""
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return []

def load_cidrs_from_file(filename: str) -> List[str]:
    """Load CIDR ranges from a text file (one per line)."""
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return []

def save_results_to_file(results: Dict[str, List[str]], filename: str):
    """Save results to a text file."""
    try:
        with open(filename, 'w') as f:
            f.write("IP Address CIDR Range Check Results\n")
            f.write("="*50 + "\n\n")
            
            for ip, ranges in results.items():
                f.write(f"IP: {ip}\n")
                if ranges:
                    f.write("  Matching CIDR ranges:\n")
                    for range_str in ranges:
                        f.write(f"    - {range_str}\n")
                else:
                    f.write("  No matching CIDR ranges found\n")
                f.write("\n")
        
        print(f"Results saved to '{filename}'")
    except Exception as e:
        print(f"Error saving results: {e}")

# Example usage with file I/O
def check_from_files(ip_file: str, cidr_file: str, output_file: str = None):
    """
    Check IPs from files and optionally save results.
    
    Args:
        ip_file: Text file with IP addresses (one per line)
        cidr_file: Text file with CIDR ranges (one per line) 
        output_file: Optional output file for results
    """
    ip_addresses = load_ips_from_file(ip_file)
    cidr_ranges = load_cidrs_from_file(cidr_file)
    
    if not ip_addresses:
        print("No IP addresses loaded")
        return
    
    if not cidr_ranges:
        print("No CIDR ranges loaded")
        return
    
    results = check_ip_in_cidr_ranges(ip_addresses, cidr_ranges)
    print_results(results)
    
    if output_file:
        save_results_to_file(results, output_file)

if __name__ == "__main__":
    main()
    
    # Uncomment to use with files instead:
    # check_from_files('ip_addresses.txt', 'cidr_ranges.txt', 'results.txt')