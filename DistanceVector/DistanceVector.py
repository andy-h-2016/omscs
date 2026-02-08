# Distance Vector project for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, Jeffrey Randow, new VM fixes by Jared Scott and James Lohse.

from Node import *
from helpers import *


class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        """ Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here."""

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)
        
        # TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data
        # distance vector is a dict
        # key: node name
        # value: weight from self to node
        self.distance_vector = {self.name: 0}

    def create_message(self):
        return (self.name, self.distance_vector)


    def send_initial_messages(self):
        """ This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight """

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py
        # compute distances for each neighbor
        # send these distances to each neighbor
        msg = self.create_message()
        for neighbor_name in self.neighbor_names:
            self.send_msg(msg, neighbor_name)


    def process_BF(self):
        """ This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. """

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # TODO 1. Process queued messages       
        change_flag = False
        for msg in self.messages:            
            (outgoing_name, advertised_dv) = msg
            (_, weight_to_outgoing_node) = self.get_outgoing_neighbor_weight(outgoing_name)
            if weight_to_outgoing_node == "Node Not Found":
                print(f"Outgoing Node {outgoing_name} Not Found for Origin Node {self.name}")
                continue
            
            # print(f"dv: {advertised_dv}")

            for dest, weight in advertised_dv.items():
                new_weight = weight_to_outgoing_node + weight
                if dest in self.distance_vector:
                    current_weight = self.distance_vector[dest]
                    if new_weight < current_weight: 
                        self.distance_vector[dest] = new_weight
                        change_flag = True
                else:
                    self.distance_vector[dest] = new_weight
                    change_flag = True
        
        # Empty queue
        self.messages = []

        # TODO 2. Send neighbors updated distances
        if change_flag:
            msg = self.create_message()
            for neighbor_name in self.neighbor_names:
                self.send_msg(msg, neighbor_name)
            

    def log_distances(self):
        """ This function is called immediately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:(A,0) (B,1) (C,-2)
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 """
        
        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided.        
        list = []
        for dest_name, dist in self.distance_vector.items():
            list.append(f"({dest_name},{dist})")
        add_entry(self.name, " ".join(list))    