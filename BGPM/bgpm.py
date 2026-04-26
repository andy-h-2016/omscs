#!/usr/bin/env python3

# Border Gateway Protocol Measurement, Copyright 2024
#
# Georgia Tech asserts copyright ownership of this template and all derivative
# works, including solutions to the projects assigned in this course. Students
# and other users of this template code are advised not to share it with others
# or to make it available on publicly viewable websites including repositories
# such as GitHub and GitLab. This copyright statement should not be removed
# or edited. Removing it will be considered an academic integrity issue.
# 
# We do grant permission to share solutions privately with non-students such
# as potential employers as long as this header remains in full. However,
# sharing with other current or future students or using a medium to share
# where the code is widely available on the internet is prohibited and
# subject to being investigated as a GT honor code violation.
# Please respect the intellectual ownership of the course materials
# (including exam keys, project requirements, etc.) and do not distribute them
# to anyone not enrolled in the class. Use of any previous semester course
# materials, such as tests, quizzes, homework, projects, videos, and any other
# coursework, is prohibited in this course.

import pybgpstream
import re

# CS 6250 BGP Measurements Project for GA Tech OMSCS CS 6250: Computer Networks
#
# Notes:
# - Edit this file according to the project description and the docstrings provided for each function
# - Do not change the existing function names or arguments
# - You may add additional functions but they must be contained entirely in this file


# Task 1A: Unique Advertised Prefixes Over Time
def unique_prefixes_by_snapshot(cache_files):
    """
    Retrieve the number of unique IP prefixes from each of the input BGP data files.

    Args:
        cache_files: A chronologically sorted list of absolute (also called "fully qualified") path names

    Returns:
        A list containing the number of unique IP prefixes for each input file.
        For example: [2, 5]
    """
    # the required return type is 'list' - you are welcome to define additional data structures, if needed
    unique_prefixes_by_snapshot = []

    for fpath in cache_files:
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "rib-file", fpath)
        unique_prefixes = set()
        count = 0
        for elem in stream:
            count += 1
            prefix = elem._maybe_field("prefix")
            unique_prefixes.add(prefix)
        unique_prefixes_by_snapshot.append(len(unique_prefixes))
        
        # implement your solution here
        print("count: ", count)
    return unique_prefixes_by_snapshot


# Task 1B: Unique Autonomous Systems Over Time
def unique_ases_by_snapshot(cache_files):
    """
    Retrieve the number of unique ASes from each of the input BGP data files.

    Args:
        cache_files: A chronologically sorted list of absolute (also called "fully qualified") path names

    Returns:
        A list containing the number of unique ASes for each input file.
        For example: [2, 5]
    """
    # the required return type is 'list' - you are welcome to define additional data structures, if needed
    unique_ases_by_snapshot = []

    for fpath in cache_files:
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "rib-file", fpath)

        # implement your solution here
        year = stream
        unique_ases = set()
        for entry in year:
            as_path = entry._maybe_field("as-path")
            if as_path == "":
                continue
            ases = as_path.strip().split(" ")
            unique_ases.update(ases)
        unique_ases_by_snapshot.append(len(unique_ases))

    return unique_ases_by_snapshot


# Task 1C: Top-10 Origin AS by Prefix Growth
def top_10_ases_by_prefix_growth(cache_files):
    """
    Compute the top 10 origin ASes ordered by percentage increase of advertised prefixes (smallest to largest)

    Args:
        cache_files: A chronologically sorted list of absolute (also called "fully qualified") path names

    Returns:
        A list of the top 10 origin ASes ordered by percentage increase of advertised prefixes (smallest to largest)
        AS numbers are represented as strings.

        For example: ["777", "1", "6"]
          corresponds to AS "777" as having the smallest percentage increase (of the top ten) and AS "6" having the
          highest percentage increase (of the top ten).
    """
    # the required return type is 'list' - you are welcome to define additional data structures, if needed
    top_10_ases_by_prefix_growth = []
    as_advertisements = {}
    for ndx, fpath in enumerate(cache_files):
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "rib-file", fpath)

        # implement your solution here
        year = stream
        print("--------------------------- new year ----------------------------")
        unique_prefixes_per_as_this_year = {}
        for entry in year:
            prefix = entry._maybe_field("prefix")

            as_path = entry._maybe_field("as-path")
            ases = as_path.strip().split(" ")
            origin_as = ases[-1]
            if origin_as in unique_prefixes_per_as_this_year:
                unique_prefixes_per_as_this_year[origin_as].add(prefix)
            else:
                unique_prefixes_per_as_this_year[origin_as] = {prefix}
    
        for origin_as, unique_prefixes_this_year in unique_prefixes_per_as_this_year.items():
            num_unique_prefixes = len(unique_prefixes_this_year)
            if origin_as in as_advertisements:
                as_advertisements[origin_as]["end"] = num_unique_prefixes
            else:
                as_advertisements[origin_as] = {"start": num_unique_prefixes, "end": num_unique_prefixes}
    
    as_by_growth = {}
    growth_rates = []
    for origin_as, advertisements in as_advertisements.items():
        start, end = advertisements.values()
        growth = 0 if start == end else (end - start) / start
        if growth in as_by_growth:
            as_by_growth[growth].append(origin_as) 
        else:
            # only include new growth rates to the list of growth rates to avoid duplicates
            growth_rates.append(growth)
            as_by_growth[growth] = [origin_as]

    growth_rates.sort(reverse=True)
    for i in range(10):
        if len(top_10_ases_by_prefix_growth) == 10:
            break
        growth = growth_rates[i]
        for a_system in as_by_growth[growth]:
            top_10_ases_by_prefix_growth.insert(0, a_system)
            if len(top_10_ases_by_prefix_growth) == 10:
                break

    return top_10_ases_by_prefix_growth

# Task 2: Routing Table Growth: AS-Path Length Evolution Over Time
def shortest_path_by_origin_by_snapshot(cache_files):
    """
    Compute the shortest AS path length for every origin AS from input BGP data files.

    Retrieves the shortest AS path length for every origin AS for every input file.

    Your code should return a dictionary where every key is a string representing an AS name and every value is a list
    of the shortest path lengths for that AS.

    Note: If a given AS is not present in an input file, the corresponding entry for that AS and file should be zero (0)
    Every list value in the dictionary should have the same length.

    Args:
        cache_files: A chronologically sorted list of absolute (also called "fully qualified") path names

    Returns:
        A dictionary where every key is a string representing an AS name and every value is a list, containing one entry
        per file, of the shortest path lengths for that AS
        AS numbers are represented as strings.

        Example:
        Given three cache files (also called "snapshots"), the results {"455": [4, 2, 3], "533": [4, 10, 2]}
        mean that AS 455 has a shortest path length of 4 in the first cache file, a shortest path length of 2 in the second
        cache file, and a shortest path of 3 in the third cache file. Similarly, AS 533 has shortest path lengths of 4, 10, and 2.
    """
    # the required return type is 'dict' - you are welcome to define additional data structures, if needed
    shortest_path_by_origin_by_snapshot = {}
    num_years = len(cache_files)

    for ndx, fpath in enumerate(cache_files):
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "rib-file", fpath)

        # implement your solution here
        year = stream
        for entry in year:
            as_path = entry._maybe_field("as-path")
            ases = as_path.strip().split(" ")
            origin_as = ases[-1]
            if origin_as == "":
                continue
            unique_ases = set()
            for auto_sys in ases:
                unique_ases.add(auto_sys)

                
            
            # scenario with AS-123 and current path of 10
            # a = {}; empty set
            # a = {'123': [1]}; first path entry for the year
            # a = {'123': [3, 5]}; path entry already exists, but is shorter than the current path
            # a = {'123': [3, 15]}; path entry already exists, but is longer than the current path
            current_path = len(unique_ases)
            current_path = 0 if current_path < 2 else current_path
            # if ndx == 1 and origin_as == "15479":
                # print("------------------------------")
                # print("as_path: ", as_path)
                # print("ases: ", ases)
                # print("unique_ases: ", unique_ases)
                # print("current_path: ", current_path)
            if origin_as in shortest_path_by_origin_by_snapshot:
                if current_path < 2:
                    continue
                shortest_path_by_year = shortest_path_by_origin_by_snapshot[origin_as]
                shortest_path = shortest_path_by_year[ndx]
                # if ndx == 1 and origin_as == "15479":
                #     print("shortest_path: ", shortest_path)
                shortest_path_by_year[ndx] = current_path if shortest_path == 0 else min(shortest_path, current_path)
            else:
                new_list = [0] * num_years
                new_list[ndx] = current_path
                # if ndx == 1 and origin_as == "15479":
                    # print("new_list: ", new_list)
                shortest_path_by_origin_by_snapshot[origin_as] = new_list

    return shortest_path_by_origin_by_snapshot


# Task 3: Announcement-Withdrawal Event Durations
def aw_event_durations(cache_files):
    """
    Identify Announcement and Withdrawal events and compute the duration of all explicit AW events in the input BGP data

    Args:
        cache_files: A chronologically sorted list of absolute (also called "fully qualified") path names

    Returns:
        A dictionary where each key is a string representing the address of a peer (peerIP) and each value is a
        dictionary with keys that are strings representing a prefix and values that are the list of explicit AW event
        durations (in seconds) for that peerIP and prefix pair.

        For example: {"127.0.0.1": {"12.13.14.0/24": [4.0, 1.0, 3.0]}}
        corresponds to the peerIP "127.0.0.1", the prefix "12.13.14.0/24" and event durations of 4.0, 1.0 and 3.0.
    """
    # the required return type is 'dict' - you are welcome to define additional data structures, if needed
    aw_event_durations = {}
    announce_times_by_ip_by_prefix = {}
    announce_times_by_ip_by_prefix = {}

    for ndx, fpath in enumerate(cache_files):
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "upd-file", fpath)
        for entry in stream:
            type = entry.type
            time = entry.time
            prefix = entry._maybe_field("prefix")
            if prefix == "":
                continue

            peer_ip = entry.peer_address
            if type == "A":
                if peer_ip in announce_times_by_ip_by_prefix:
                    announce_times_by_prefix = announce_times_by_ip_by_prefix[peer_ip]
                    announce_times_by_prefix[prefix] = time
                else:
                    announce_times_by_ip_by_prefix[peer_ip] = {prefix: time}
            elif type == "W":
                # skip if a corresponding announce time does not exist
                if peer_ip not in announce_times_by_ip_by_prefix:
                    continue

                announce_times_by_prefix = announce_times_by_ip_by_prefix[peer_ip]
                if prefix not in announce_times_by_prefix:
                    continue

                announce_time = announce_times_by_prefix[prefix]
                
                # skip if announce time and explicit withdraw time are the same
                # if so, clear the announce time (canceled out by the withdraw time)
                if time == announce_time:
                    del announce_times_by_ip_by_prefix[peer_ip][prefix]
                    continue

                duration = time - announce_time
                if peer_ip in aw_event_durations:
                    durations_by_prefix = aw_event_durations[peer_ip]
                    if prefix in durations_by_prefix:
                        durations_by_prefix[prefix].append(duration)
                    else:
                        durations_by_prefix[prefix] = [duration]
                else:
                    aw_event_durations[peer_ip] = {prefix: [duration]}

                # remove announcement once the duration is calculated
                del announce_times_by_ip_by_prefix[peer_ip][prefix]
    return aw_event_durations


# Task 4: RTBH Event Durations
def rtbh_event_durations(cache_files):
    """
    Identify blackholing events and compute the duration of all RTBH events from the input BGP data

    Identify events where the prefixes are tagged with at least one Remote Triggered Blackholing (RTBH) community.

    Args:
        cache_files: A chronologically sorted list of absolute (also called "fully qualified") path names

    Returns:
        A dictionary where each key is a string representing the address of a peer (peerIP) and each value is a
        dictionary with keys that are strings representing a prefix and values that are the list of explicit RTBH event
        durations (in seconds) for that peerIP and prefix pair.

        For example: {"127.0.0.1": {"12.13.14.0/24": [4.0, 1.0, 3.0]}}
        corresponds to the peerIP "127.0.0.1", the prefix "12.13.14.0/24" and event durations of 4.0, 1.0 and 3.0.
    """
    # the required return type is 'dict' - you are welcome to define additional data structures, if needed
    rtbh_event_durations = {}
    announce_times_by_ip_by_prefix = {}
    for fpath in cache_files:
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "upd-file", fpath)

        # implement your solution here
        for entry in stream:
            type = entry.type
            time = entry.time
            prefix = entry._maybe_field("prefix")
            if prefix == "":
                continue

            communities = " ".join(entry.fields["communities"]) if "communities" in entry.fields else ""
            peer_ip = entry.peer_address
            if type == "A":
                match = re.search(r"\:666\b", communities)
                if match:        
                    if peer_ip in announce_times_by_ip_by_prefix:
                        announce_times_by_prefix = announce_times_by_ip_by_prefix[peer_ip]
                        announce_times_by_prefix[prefix] = time
                    else:
                        announce_times_by_ip_by_prefix[peer_ip] = {prefix: time}
                elif peer_ip in announce_times_by_ip_by_prefix:
                    if prefix in announce_times_by_ip_by_prefix[peer_ip]:
                        del announce_times_by_ip_by_prefix[peer_ip][prefix]
            elif type == "W":
                # skip if a corresponding announce time does not exist
                if peer_ip not in announce_times_by_ip_by_prefix:
                    continue

                announce_times_by_prefix = announce_times_by_ip_by_prefix[peer_ip]
                if prefix not in announce_times_by_prefix:
                    continue

                if peer_ip == "2001:7f8::71d4:0:1" and prefix == "2600:1417:3e::/48":
                    print("announce_time: ", announce_times_by_prefix[prefix])
                    print("duration: ", time - announce_times_by_prefix[prefix])

                announce_time = announce_times_by_prefix[prefix]
                
                # skip if announce time and explicit withdraw time are the same
                # if so, clear the announce time (canceled out by the withdraw time)

                if time == announce_time:
                    del announce_times_by_ip_by_prefix[peer_ip][prefix]
                    continue

                duration = time - announce_time
                if peer_ip in rtbh_event_durations:
                    durations_by_prefix = rtbh_event_durations[peer_ip]
                    if prefix in durations_by_prefix:
                        durations_by_prefix[prefix].append(duration)
                    else:
                        durations_by_prefix[prefix] = [duration]
                else:
                    rtbh_event_durations[peer_ip] = {prefix: [duration]}

                # remove announcement once the duration is calculated
                del announce_times_by_ip_by_prefix[peer_ip][prefix]

    return rtbh_event_durations
