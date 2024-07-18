import tkinter as tk
from tkinter import scrolledtext
import sys
from io import StringIO

class DraggableCodeBlock(tk.Frame):

    def __init__(self, master, Text, Code_Area, All_Blocks, loop=False):
        super().__init__(master, bd=2)

        self.Code_Area = Code_Area
        self.All_Blocks = All_Blocks
        self.loop = loop

        self.label = tk.Label(self, text=Text, relief="raised")
        self.label.pack(side=tk.LEFT)

        if self.loop:
            self.loop_amount_entry = tk.Entry(self, width=5)
            self.loop_amount_entry.insert(0, "10")  # Default to 10
            self.loop_amount_entry.pack(side=tk.LEFT)

        self.pack_propagate(False)  # Prevent the frame from resizing to fit its children
        self.config(width=250, height=30)  # Set a fixed size for the frame

        # Bind drag events to the entire frame
        self.bind("<Button-1>", self.On_Click)
        self.bind("<B1-Motion>", self.On_Drag)
        self.bind("<ButtonRelease-1>", self.On_Release)

    def On_Click(self, event):
        self.Drag_Data = {"x": event.x, "y": event.y}

    def On_Drag(self, event):
        x = self.winfo_x() - self.Drag_Data["x"] + event.x
        y = self.winfo_y() - self.Drag_Data["y"] + event.y
        self.place(x=x, y=y)

    def On_Release(self, event):
        Closest_Block, Position = self.Find_Closest_Block()
        if Closest_Block:
            if Position == "above":
                self.Snap_To_Block(Closest_Block, "below")
            elif Position == "below":
                self.Snap_To_Block(Closest_Block, "above")

    def Find_Closest_Block(self):
        Minimum_Distance_Above = float('inf')
        Minimum_Distance_Below = float('inf')
        Closest_Block_Above = None
        Closest_Block_Below = None

        snap_distance = 10  # Adjust this value for smaller snapping distance

        for Block in self.All_Blocks:
            if Block == self:
                continue

            Distance_Above = abs(self.winfo_y() - (Block.winfo_y() + Block.winfo_height()))
            Distance_Below = abs((self.winfo_y() + self.winfo_height()) - Block.winfo_y())

            if Distance_Above < Minimum_Distance_Above and Distance_Above < snap_distance:
                Minimum_Distance_Above = Distance_Above
                Closest_Block_Above = Block

            if Distance_Below < Minimum_Distance_Below and Distance_Below < snap_distance:
                Minimum_Distance_Below = Distance_Below
                Closest_Block_Below = Block

        return (Closest_Block_Above if Minimum_Distance_Above < Minimum_Distance_Below else Closest_Block_Below, 
                "above" if Minimum_Distance_Above < Minimum_Distance_Below else "below")

    def Snap_To_Block(self, Block, Position):
        new_x = Block.winfo_x()
        new_y = Block.winfo_y()

        if Position == "above":
            new_y -= self.winfo_height()
        elif Position == "below":
            new_y += Block.winfo_height()

        # Check if the new position is free
        if not self.Is_Position_Occupied(new_x, new_y):
            self.place(x=new_x, y=new_y)

    def Is_Position_Occupied(self, x, y):
        for Block in self.All_Blocks:
            if Block != self:
                if (x < Block.winfo_x() + Block.winfo_width() and
                    x + self.winfo_width() > Block.winfo_x() and
                    y < Block.winfo_y() + Block.winfo_height() and
                    y + self.winfo_height() > Block.winfo_y()):
                    return True
        return False

    def get_loop_amount(self):
        if self.loop:
            try:
                return int(self.loop_amount_entry.get())
            except ValueError:
                return 1  # Return default if conversion fails
        return 1  # Default for non-loop blocks


class Called_Function:
    @staticmethod
    def hello_world():
        return "console.log('Hello, world!');"

    @staticmethod
    def different():
        return "console.warn('Block 2');"


class Function_Class:
    @staticmethod
    def Loop(amount, code_lines):
        loop_code = [f"for(let i = 0; i < {amount}; i++){{"]
        loop_code.extend(code_lines)
        loop_code.append("}")
        return loop_code


class World:
    @staticmethod
    def world_event_1():
        return "console.log('World Event 1');"

    @staticmethod
    def world_event_2():
        return "console.log('World Event 2');"


class System:
    @staticmethod
    def system_code_1():
        return "console.log('System Code 1');"

    @staticmethod
    def system_code_2():
        return "console.log('System Code 2');"


class CodeEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Custom Code Editor")
        self.geometry("800x600")
        self.Code_Area = scrolledtext.ScrolledText(self, width=80, height=20)
        self.Code_Area.pack(pady=10)
        self.Code_Area.config(state=tk.DISABLED)  # Make the Code_Area read-only

        self.Blocks = []
        self.Create_Code_Blocks()

        Run_Button = tk.Button(self, text="Generate JSON", command=self.Run_Code)
        Run_Button.pack(pady=10)

        self.Output_Stream = StringIO()
        sys.stdout = self

    def write(self, message):
        self.Code_Area.config(state=tk.NORMAL)  # Enable the Code_Area to write
        self.Code_Area.insert(tk.END, message)
        self.Code_Area.yview(tk.END)
        self.Code_Area.config(state=tk.DISABLED)  # Make the Code_Area read-only again

    def flush(self):
        pass

    def Create_Code_Blocks(self):
        block1 = DraggableCodeBlock(self, "Called_Function.hello_world()", self.Code_Area, self.Blocks)
        block1.place(x=50, y=50)
        self.Blocks.append(block1)

        block2 = DraggableCodeBlock(self, "Function_Class.Loop()", self.Code_Area, self.Blocks, loop=True)
        block2.place(x=50, y=100)
        self.Blocks.append(block2)

        block3 = DraggableCodeBlock(self, "Called_Function.different()", self.Code_Area, self.Blocks)
        block3.place(x=50, y=150)
        self.Blocks.append(block3)

        # Add World event blocks
        block4 = DraggableCodeBlock(self, "World.world_event_1()", self.Code_Area, self.Blocks)
        block4.place(x=50, y=200)
        self.Blocks.append(block4)

        block5 = DraggableCodeBlock(self, "World.world_event_2()", self.Code_Area, self.Blocks)
        block5.place(x=50, y=250)
        self.Blocks.append(block5)

        # Add System code blocks
        block6 = DraggableCodeBlock(self, "System.system_code_1()", self.Code_Area, self.Blocks)
        block6.place(x=50, y=300)
        self.Blocks.append(block6)

        block7 = DraggableCodeBlock(self, "System.system_code_2()", self.Code_Area, self.Blocks)
        block7.place(x=50, y=350)
        self.Blocks.append(block7)

    def Get_Ordered_Blocks(self):
        return sorted(self.Blocks, key=lambda block: block.winfo_y())

    def Run_Code(self):
        Ordered_Blocks = self.Get_Ordered_Blocks()
        output_code = []
        start_processing = False

        for Block in Ordered_Blocks:
            block_text = Block.label.cget("text")

            if block_text.startswith("World.world_event_") or block_text.startswith("System.system_code_"):
                start_processing = True
                continue  # Skip the event/system blocks themselves

            if start_processing:
                if "Function_Class.Loop" in block_text:
                    loop_amount = Block.get_loop_amount()
                    loop_code = []
                    loop_block_y = Block.winfo_y() + Block.winfo_height()
                    
                    # Collect lines of blocks that are snapped directly below the loop block
                    for sub_block in Ordered_Blocks:
                        if sub_block.winfo_y() == loop_block_y and sub_block != Block:
                            sub_block_text = sub_block.label.cget("text")
                            if sub_block_text.startswith("Called_Function."):
                                sub_block_function = sub_block_text.split(".")[1].replace("()", "")
                                loop_code.append(getattr(Called_Function, sub_block_function)())
                            loop_block_y += sub_block.winfo_height()

                    output_code.extend(Function_Class.Loop(loop_amount, loop_code))

                # Process World and System blocks
                if block_text.startswith("World."):
                    block_function = block_text.split(".")[1].replace("()", "")
                    output_code.append(getattr(World, block_function)())
                elif block_text.startswith("System."):
                    block_function = block_text.split(".")[1].replace("()", "")
                    output_code.append(getattr(System, block_function)())

        # Reset and update Code_Area with generated code
        self.Code_Area.config(state=tk.NORMAL)  # Enable the Code_Area to write
        self.Code_Area.delete(1.0, tk.END)  # Clear the Code_Area
        self.Code_Area.insert(tk.END, "\n".join(output_code))
        self.Code_Area.config(state=tk.DISABLED)  # Make the Code_Area read-only again

        self.Output_Stream.truncate(0)
        self.Output_Stream.seek(0)

if __name__ == "__main__":
    editor = CodeEditor()
    editor.mainloop()
