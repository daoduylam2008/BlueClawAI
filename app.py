from textual.app import App
from textual.widgets import Input, Label
from textual.containers import VerticalScroll
from textual.color import Color
from textual.reactive import reactive
from textual import on

import requests
from urllib3 import response


logo = """
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%█████%%%%%%%████%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%██████%%%%%██████%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%██████%%%%███████%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%██████%%%%████████%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%█████%%%%%████████%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%████████%%%%%███%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%████████%%%%██████%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%███████%%%%██████%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%██████%%%%%%█████%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%█████%%%%%%█████%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""


logo = logo.replace("%", " ")
URL = 'http://127.0.0.1:8080'
blue = Color(104, 144, 229)


def request(message=None):
    """
    Request to run the llm model.
    """
    # If args.query is None, which means user is in loop and allowed to ask directly to the model without using arguments.
    params = {
        "query": message
    }

    response = requests.get(f'{URL}/request/', params=params)

    if response.status_code == 200:
        data = response.json()
        
        return data
    else:
        print(f"Error: Received status code {response.status_code}")

        return {
            "ai_response": None,
            "tool_response": None,
            "human_response": None,
            "error": f"{response.status_code}"
        }


class BlueClawApp(App):
    CSS = """
    Label {
        margin-bottom: 1 ;
        margin-top: 1;
    }
    """

    def compose(self):
        self.layout = VerticalScroll()
        self.logo = Label(logo)
        self.version = Label("BlueClawAI Terminal v1.1.0")
        self.welcome = Label("Welcome back!")

        # Input layout
        self.prompt = Input(
            placeholder="How can I help you today?", 
            )

        with self.layout:
            yield self.logo
            yield self.version
            yield self.welcome


        yield self.prompt

    def on_mount(self):
        self.layout.styles.border = ("solid", blue)
        self.layout.styles.align_horizontal = "center"
        self.layout.styles.height = "90%"
        self.layout.scroll_end(animate=False)

        self.welcome.styles.color = blue

        self.logo.styles.color = blue
        self.logo.styles.width = "90%"
        self.logo.styles.content_align_horizontal = "center"

        self.version.styles.color = Color(255, 243, 79)

        self.prompt.styles.border_bottom = ("solid", blue)
        self.prompt.styles.border_top = ("solid", blue)



    
    @on(Input.Submitted)
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """An event handler called when input is submitted."""
        user_label = Label("> " + self.prompt.value)
        user_label.styles.width = "80%"
        user_label.styles.background = Color(46,46,46)
        
        self.layout.mount(user_label)
        # Request to the model with user input just has submitted
        responses = request(self.prompt.value)
        if responses["ai_response"] != None:
            response_label = Label("⎿ " + responses["ai_response"])
        else:
            response_label = Label("")
        response_label.styles.width = "80%"
        response_label.styles.color = blue
        self.layout.mount(response_label)

        self.prompt.value = ""

        self.layout.scroll_end(animate=False)


        
    def _on_key(self, event) -> None:
        if event.key == "ctrl+c":
            event.prevent_default()
            self.exit()

if __name__ == "__main__":
    app = BlueClawApp()
    app.run()