import pygame
import random
import time


class Graph():
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.edgeRank = []
        self.selected_node = None
        self.collored = False
        self.collors = 0
        self.id = 0

    def addNode(self, node):
        node.setName(self.id)
        self.edgeRank.append(self.id)
        self.nodes[self.id] = node 
        self.id += 1
    
    def deleteNode(self, node):
        nod = 0
        print(self.nodes)
        while nod < len(self.nodes[node].linked_to):
            self.nodes[self.nodes[self.nodes[node].linked_to[nod]].name].edges -= 1
            i = 0
            while i < len(self.nodes[self.nodes[node].linked_to[nod]].linked_to):
                if self.nodes[self.nodes[node].linked_to[nod]].linked_to[i] == node:
                    self.nodes[self.nodes[self.nodes[node].linked_to[nod]].name].linked_to.pop(i)
                    break
                i += 1
            nod += 1
        
        i = 0
        while i < len(self.edges):
            if node in self.edges[i]:
                self.edges.pop(i)
                i -= 1
            i += 1
                
        del self.nodes[node]
        for i in range(len(self.edgeRank)):
            if self.edgeRank[i] == node:
                self.edgeRank.pop(i)
                break
    
    def connectNode(self, from_n, to_n):
        for i in self.edges:
            if from_n in i and to_n in i:
                return
        
        self.edges.append((from_n, to_n))
        self.nodes[from_n].edges += 1
        self.nodes[to_n].edges += 1
        self.nodes[from_n].linked_to.append(to_n)
        self.nodes[to_n].linked_to.append(from_n)
    
    def Sort(self):
       for i in range(1, len(self.edgeRank)):
        index_awal = i
        index_banding = i - 1
        while self.nodes[self.edgeRank[index_awal]].edges > self.nodes[self.edgeRank[index_banding]].edges and index_banding >= 0:
            self.edgeRank[index_banding], self.edgeRank[index_awal] = self.edgeRank[index_awal], self.edgeRank[index_banding]
            index_banding = index_banding - 1
            index_awal -= 1

    
    def drawNodes(self, win):
        for i in self.nodes:
            self.nodes[i].drawNode(win)
    
    def drawEdges(self, win):
        for i in self.edges:
            pygame.draw.line(win, (0, 0, 0), self.nodes[i[0]].pos, self.nodes[i[1]].pos, 3)
    
    def setSelectedNode(self, mouse_pos , rad):
        for i in self.nodes:
            if (mouse_pos[0] - self.nodes[i].pos[0]) ** 2 + (mouse_pos[1] - self.nodes[i].pos[1]) ** 2 <= rad**2:
                self.selected_node = i
                break
    
    def collorizing(self, win):
        print(self.edgeRank)
        self.Sort()
        print(self.edgeRank)
        collor = []
        collored_node = []

        for i in self.edgeRank:
            if i in collored_node:
                continue

            collor_temp = self.randomCollor()

            while collor_temp in collor:
                collor_temp = self.randomCollor()
            collor.append(collor_temp)
            self.nodes[i].setCollor(collor_temp)
            collored_node.append(i)
            self.drawNodes(win)
            pygame.display.flip()
            time.sleep(1)
            collored_node_temp = []

            for j in self.nodes:
                if j in collored_node:
                    continue
                have_neighbour = False
                for k in collored_node_temp:
                    if self.nodes[j].name in self.nodes[k].linked_to:
                        have_neighbour = True
                        break
                
                if self.nodes[j].name not in self.nodes[i].linked_to and not have_neighbour:
                    self.nodes[j].setCollor(collor_temp)
                    collored_node.append(j)
                    collored_node_temp.append(j)
                    self.drawNodes(win)
                    pygame.display.flip()
                    time.sleep(1)

        self.collors = len(collor)


        # for i in range(len(self.edgeRank)):
        #     if self.edgeRank[i] in collored_node:
        #         continue

        #     collor_temp = self.randomCollor()
        #     while collor_temp in collor:
        #         collor_temp = self.randomCollor()
        #     collor.append(collor_temp)

        #     self.nodes[i].setCollor(collor_temp)
        #     collored_node.append(self.edgeRank[i])
        #     self.drawNodes(win)
        #     pygame.display.flip()
        #     time.sleep(1)
        #     for j in self.nodes:
        #         have_neighbour_color = False
        #         for c_n in collored_node:
        #             if c_n in self.nodes[j].linked_to:
        #                have_neighbour_color = True
        #                break
                
        #         if not have_neighbour_color and self.nodes[j].name not in self.nodes[self.edgeRank[i]].linked_to:
        #             self.nodes[j].setCollor(collor_temp)
        #             collored_node.append(self.nodes[j].name)
        #             self.drawNodes(win)
        #             pygame.display.flip()
        #             time.sleep(1)

        print(collor)
    def randomCollor(self):
        return (random.randint(50, 150), random.randint(50, 150), random.randint(50, 150))
    

    

