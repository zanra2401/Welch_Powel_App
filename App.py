import pygame
from deps.Node import Node
from deps.Graph import Graph
from enum import Enum

State = Enum("State", ["ADDING", "DELETING", "CONNECTING", "IDLE"])
screen_size = (1000, 800)

class UiButton:
    def __init__(self, win, x,y,w,h, collor, text_collor, text):
        self.win = win
        self.collor = collor
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.Font(None, 20)
        self.text_surface = self.font.render(text, True, text_collor)
        self.drawRect()
        self.drawText()
    
    def drawRect(self):
        pygame.draw.rect(self.win, self.collor, self.rect)

    def drawText(self):
        self.win.blit(self.text_surface, (self.rect.x + 10, self.rect.y + 10))

class App:
    def __init__(self, screen_size):
        pygame.init()
        pygame.font.init()
        self.state = State.IDLE
        self.is_running = True
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.setFps()
        self.bg = "white"
        self.connect = []
        self.node_rad = 20
        self.sideBar = pygame.Rect(700, 0 ,300,800)
        self.font = pygame.font.Font(None, 20)
        self.state_string = "Normal"

    def setFps(self, fps = 60):
        self.clock.tick(fps)
    def test(self):
        UiButton(self.screen, self.sideBar.x, self.sideBar.y, 60, 30, (255,255,255),(0,0,0), "Node" )
    
    def display_graph_stat(self, graph):
        j = 1
        for i in graph.nodes:
            text = self.font.render(f"d({graph.nodes[i].name}): {graph.nodes[i].edges}", True, (10, 10, 10, 10))
            self.screen.blit(text, (self.sideBar.x + 10, self.sideBar.y + (j * 20) + 20))
            j += 1
        text = self.font.render(f"Warna: {graph.collors}", True, (10, 10, 10, 10))
        self.screen.blit(text, (self.sideBar.x + 10, self.sideBar.y + (j * 20) + 20))
        j+=1
        text = self.font.render(f"Nodes: {len(graph.nodes)}", True, (10, 10, 10))
        self.screen.blit(text, (self.sideBar.x + 10, self.sideBar.y + (j * 20) + 20))
        j += 1
        text = self.font.render(f"Edges: {len(graph.edges)}", True, (10, 10, 10))
        self.screen.blit(text, (self.sideBar.x + 10, self.sideBar.y + (j * 20) + 20))
            

if __name__ == "__main__":
    app = App(screen_size)
    graph = Graph() 
    while app.is_running:
        app.screen.fill(app.bg)
        graph.drawEdges(app.screen)
        graph.drawNodes(app.screen)
        pygame.draw.rect(app.screen, (250,231,231), app.sideBar)
        app.test()

        

        app.display_graph_stat(graph)
        mode = pygame.font.Font(None, 25).render(f"Mode: {app.state_string}", False, (0, 0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if app.state == State.ADDING and pygame.mouse.get_pos()[0] < app.sideBar.x:
                        graph.addNode(Node(pygame.mouse.get_pos()))
                    elif app.state == State.CONNECTING:
                        graph.setSelectedNode(pygame.mouse.get_pos(), app.node_rad)
                        if graph.selected_node is not None and graph.selected_node not in app.connect:
                            app.connect.append(graph.selected_node)
                            graph.selected_node = None
                    elif app.state == State.IDLE:
                        graph.setSelectedNode(pygame.mouse.get_pos(), app.node_rad)
                    elif app.state == State.DELETING:
                        graph.setSelectedNode(pygame.mouse.get_pos(), app.node_rad)
                        if graph.selected_node != None:
                            graph.deleteNode(graph.selected_node)
                        graph.selected_node = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    app.state = State.CONNECTING
                    app.state_string = "Menghubungkan"
                elif event.key == pygame.K_a:
                    app.state = State.ADDING
                    app.state_string = "Menambahkan"
                elif event.key == pygame.K_l:
                    graph.collorizing(app.screen)
                elif event.key == pygame.K_d:
                    app.state = State.DELETING
                    app.state_string = "Menghapus"
                elif event.key == pygame.K_i:
                    app.state = State.IDLE
                    app.state_string = "Normal"
            elif event.type == pygame.MOUSEMOTION:
                if app.state == State.IDLE and graph.selected_node is not None and pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[1] > 0 and pygame.mouse.get_pos()[0] < 700 and pygame.mouse.get_pos()[1] < screen_size[1]:
                    graph.nodes[graph.selected_node].pos = pygame.mouse.get_pos()
                
            elif event.type == pygame.MOUSEBUTTONUP:
                if app.state == State.IDLE:
                    graph.selected_node = None
           
        if len(app.connect) == 2 and app.state == State.CONNECTING:
            graph.connectNode(app.connect[0], app.connect[1])
            app.connect = []
            graph.selected_node = None
        
        app.screen.blit(mode, (10, 10))
        


        

        pygame.display.flip()
        app.setFps()

            
        
