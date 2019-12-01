class RelatedRhymes:
    """Class to find words that rhyme based on graphs of related words and
    rhyming words
    """
    def __init__(self, rhyming_graph):
        """[summary]
        
        Arguments:
            rhyming_graph {Graph} -- A graph of words that are known to rhyme
        """
        self.rhyming_graph = rhyming_graph
        self.rhyming_related_lists = []

    def __call__(self, related_graph):
        """Callable implementation to permit using this class as a callback
        
        Arguments:
            related_graph {Graph} -- Graph of related words
        
        Returns:
            list -- Words that are related and rhyme
        """
        if related_graph is not None:
            return self.find_rhyming_related_words(related_graph)
    
    def find_rhyming_related_words(self, related_graph):
        """Finds words that rhyme and are related
        
        Arguments:
            related_graph {Graph} -- A graph of words that are related
        
        Returns:
            list -- Words that are related and rhyme
        """
        
        for related_word in related_graph.nodes:
            found_words = [related_word]
            related_node = related_graph.nodes[related_word]

            # Skip word because it's not part of a rhyming group
            if related_word not in self.rhyming_graph.nodes:
                continue

            # Check if the related neighbors of related_word are in the
            # same rhyming group
            for related_neighbor_word in related_node.neighbors:
                if related_neighbor_word in self.rhyming_graph.nodes[related_word].neighbors:
                    # Add related_word to a list of words that rhyme
                    found_words.append(related_neighbor_word)
                    self.rhyming_graph.delete_node(related_neighbor_word)

            if len(found_words) > 1:
                self.rhyming_related_lists.append(found_words)

        return self.rhyming_related_lists

    def clear(self):
        self.rhyming_related_lists = []