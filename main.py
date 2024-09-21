try:
    import sys
    import pygame
    import pygame_gui
except ImportError as err:
    print(f"Couldn't load module: {err}")
    sys.exit(1)


#Base class to handle window management and basic UI functions.
class Window:
    def __init__(self, window, ui, text_font, width, height):
        self.screen = window
        self.manager = ui
        self.font = text_font
        self.width = width
        self.height = height
        self.running = True
        self.clock = pygame.time.Clock()
        self.background_colour = (251, 150, 138)
        self.title_colour = (255, 255, 255)

    #Function to render text
    def render_text(self, text, x, y, colour):
        text_surface = self.font.render(text, True, colour)
        self.screen.blit(text_surface, (x, y))

    #Function to create buttons
    @staticmethod
    def create_buttons(text, x, y):
        button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x, y), (100, 50)),
                                                              text=text,
                                                              manager=manager)
        return button

    #Function to output list values and change colour when appropiate
    def list_values(self, data):
        for idx, value in enumerate(data):
            if idx in self.swap_indices and not self.swap:
                colour = (255, 0, 0)
            elif idx in self.swap_indices and self.swap:
                colour = (0, 255, 0)
            else:
                colour = (255, 255, 255)
            self.render_text(str(value), self.center_x-75 + idx * 30, self.center_y, colour)


#Class for the input box
class InputBox:
    def __init__(self, x, y, width, height, ui):
        self.rect = pygame.Rect(x, y, width, height)
        self.manager = ui
        self.text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((x, y), (100, 50)),manager=self.manager)
        self.text = ''
        self.visible = True

    def get_text(self):
        return self.text_entry.get_text()

    def draw(self, ui):
        if self.visible:
            self.manager.draw_ui(ui)

    def update(self, time_delta):
        if self.visible:
            self.manager.update(time_delta)

    def handle_event(self, event):
        if self.visible:
            self.manager.process_events(event)

    def toggle_visibility(self):
        self.visible = not self.visible
        self.text_entry._set_visible(self.visible)

#Class for main menu
class MainMenu(Window):
    def __init__(self, window, ui, text_font, width, height):
        super().__init__(window, ui, text_font, width, height)

        self.center_x = (self.width / 2) - 50
        self.center_y = (self.height / 2) - 25
        self.algorithms_button = self.create_buttons('Algorithms', self.center_x-100, self.center_y)

        self.quit_button = self.create_buttons('Quit', self.center_x+100, self.center_y)
        self.title_text = 'pySorter'

    def run(self):
        while self.running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.algorithms_button:
                        self.running = False
                        algorithms_menu = AlgorithmsMenu(self.screen, self.manager, self.font, self.width, self.height)
                        self.hide()
                        algorithms_menu.run()
                    elif event.ui_element == self.quit_button:
                        self.running = False

                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.screen.fill(self.background_colour)
            self.render_text(self.title_text, self.center_x-20, self.height - 750, self.title_colour)
            self.manager.draw_ui(self.screen)
            pygame.display.update()

    def hide(self):
        self.algorithms_button.hide()
        self.quit_button.hide()


#Class for the algorithms menu
class AlgorithmsMenu(Window):
    def __init__(self, window, ui, text_font, width, height):
        super().__init__(window, ui, text_font, width, height)
        self.center_x = (self.width / 2) - 50
        self.center_y = (self.height / 2) - 25
        self.selection_sort = self.create_buttons('Selection Sort', self.center_x, self.center_y)
        self.insertion_sort = self.create_buttons('Insertion Sort', self.center_x + 150, self.center_y)
        self.bubble_sort = self.create_buttons('Bubble Sort', self.center_x - 150, self.center_y)
        self.back_button = self.create_buttons('Back', 0, 750)
        self.swap_indices = (-1, -1)
    def run(self):
        while self.running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.selection_sort:
                        self.running = False
                        self.hide()
                        selection_sort = SelectionSort(self.screen, self.manager, self.font, self.width, self.height)
                        selection_sort.run()
                    elif event.ui_element == self.insertion_sort:
                        self.running = False
                        self.hide()
                        insertion_sort = InsertionSort(self.screen, self.manager, self.font, self.width, self.height)
                        insertion_sort.run()
                    elif event.ui_element == self.bubble_sort:
                        self.running = False
                        self.hide()
                        bubble_sort = BubbleSort(self.screen, self.manager, self.font, self.width, self.height)
                        bubble_sort.run()
                    elif event.ui_element == self.back_button:
                        self.running = False
                        self.hide()
                        main_menu = MainMenu(self.screen, self.manager, self.font, self.width, self.height)
                        main_menu.run()
                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.screen.fill(self.background_colour)
            self.render_text("Select an algorithm",self.center_x-100 ,self.height - 750, self.title_colour)
            self.manager.draw_ui(self.screen)
            pygame.display.update()

    def hide(self):
        self.selection_sort.hide()
        self.insertion_sort.hide()
        self.bubble_sort.hide()
        self.back_button.hide()


#Base class for the individual sorting algorithms
class SortingAlgorithmBase(Window):
    def __init__(self, window, ui, text_font, width, height):
        super().__init__(window, ui, text_font, width, height)
        self.center_x = (self.width / 2) - 50
        self.center_y = (self.height / 2) - 25
        self.input_box = InputBox(self.center_x, self.center_y + 100, 200, 50, self.manager)
        self.data = None
        self.sorted = None
        self.sort_in_progress = None
        self.swap_indices = (-1, -1)
        self.swap = False
        self.back_button = self.create_buttons('Back', 0, 750)


    def run(self):
        while self.running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.data = self.input_box.get_text()
                    if event.key == pygame.K_RETURN and self.data is not None:
                      self.sorted = list(self.data)
                      self.sort_in_progress = self.sort(self.sorted)
                    elif event.key == pygame.K_RIGHT and self.sort_in_progress is not None:
                        try:
                            #Continues iteration
                            next(self.sort_in_progress)
                        except StopIteration:
                            #Stops if there's none left
                            self.sort_in_progress = None
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.back_button:
                        self.running = False
                        self.hide()
                        algorithms_menu = AlgorithmsMenu(self.screen, self.manager, self.font, self.width, self.height)
                        algorithms_menu.run()
                self.input_box.handle_event(event)
            self.input_box.update(time_delta)
            self.screen.fill(self.background_colour)
            self.render_text("Input data to be sorted",self.center_x-100,self.height - 750, self.title_colour)
            self.manager.draw_ui(self.screen)
            self.input_box.draw(self.screen)
            if self.sorted:
                self.list_values(self.sorted)
            pygame.display.update()

    def hide(self):
        self.back_button.hide()
        self.input_box.toggle_visibility()


#Selection Sort Class
class SelectionSort(SortingAlgorithmBase):
    def __init__(self, window, ui, text_font, width, height):
        super().__init__(window, ui, text_font, width, height)


    def sort(self, data):
        try:
            for i in range(len(data)):
                cur_min_idx = i
                for j in range(i + 1, len(data)):
                    if data[j] < data[cur_min_idx]:
                        cur_min_idx = j
                self.swap_indices = (i, cur_min_idx)
                self.swap = False
                yield data
                data[i], data[cur_min_idx] = data[cur_min_idx], data[i]
                self.swap = True
                self.swap_indices = (i, cur_min_idx)
                #Pauses after each swap
                yield data

        except ValueError:
            pass


#Insertion Sort class
class InsertionSort(SortingAlgorithmBase):
    def __init__(self, window, ui, text_font, width, height):
        super().__init__(window, ui, text_font, width, height)

    def sort(self, data):
        try:
            for i in range(1, len(data)):
                j = i - 1
                while j >= 0 and data[j+1] < data[j]:
                    self.swap_indices = (j, j+1)
                    self.swap = False
                    yield data
                    data[j], data[j+1] = data[j+1], data[j]
                    self.swap = True
                    self.swap_indices = (j, j+1)
                    yield data
                    j -= 1
            return data
        except ValueError:
            pass



#Bubble Sort class
class BubbleSort(SortingAlgorithmBase):
    def __init__(self, window, ui, text_font, width, height):
        super().__init__(window, ui, text_font, width, height)

    def sort(self, data):
        try:
            for i in range(len(data)):
                for j in range(i+1, len(data)):
                    if data[j] < data[i]:
                        self.swap_indices = (i, j)
                        self.swap = False
                        yield data
                        data[i], data[j] = data[j], data[i]
                        self.swap = True
                        self.swap_indices = (i, j)
                        yield data
            return data
        except ValueError:
            pass




# Initialize pygame
pygame.init()
pygame.font.init()

# Set titlebar
pygame.display.set_caption("pySorter")

#Initilise parameters
screen = pygame.display.set_mode((800, 800))
manager = pygame_gui.UIManager((800, 800), theme_path="UI.json")
font = pygame.font.Font(None, 50)
screen_width = screen.get_width()
screen_height = screen.get_height()

#Run main menu function
main_menu = MainMenu(screen, manager, font, screen_width, screen_height)
main_menu.run()

pygame.quit()
