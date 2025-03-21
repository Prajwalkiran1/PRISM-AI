import customtkinter as ctk
import threading
import time
from PIL import Image, ImageTk
from voice_assistant_model import VoiceAssistantModel
import math
import os

class VoiceAssistantUI:
    def __init__(self):
        self.model = VoiceAssistantModel()
       
        self.window = ctk.CTk()
        self.window.title("PRISM AI")
        self.window.geometry("1100x800")
        ctk.set_appearance_mode("dark")
       
        self.colors = {
            "bg_primary": "#0f111a",
            "bg_secondary": "#1a1c25",
            "bg_tertiary": "#252836",
            "accent_primary": "#6c5ce7",
            "accent_secondary": "#00cec9",
            "accent_tertiary": "#a29bfe",
            "text_primary": "#ffffff",
            "text_secondary": "#ced4da",
            "text_tertiary": "#8d93ab",
            "user_msg": "#74b9ff",
            "assistant_msg": "#00b894",
            "system_msg": "#fd79a8",
            "alert": "#ff7675",
            "shadow": "rgba(0, 0, 0, 0.2)"
        }
       
        self.animation_active = False
        self.animation_frame = 0
       
        self.setup_ui()
        self.setup_animations()
       
        self.update_chat(f"Welcome! I'm in {self.model.current_personality} mode. How can I help you today?", "assistant")

    def setup_animations(self):
        self.animation_timer = self.window.after(50, self.update_animations)

    def update_animations(self):
        if self.animation_active:
            self.animation_frame += 1
            pulse = abs(math.sin(self.animation_frame * 0.1)) * 10
           
            if hasattr(self, 'mic_button') and self.model.is_listening:
                glow_color = self.adjust_color_brightness(self.colors["alert"], pulse/10)
                self.mic_button.configure(border_color=glow_color)
       
        self.animation_timer = self.window.after(50, self.update_animations)

    def adjust_color_brightness(self, hex_color, factor):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
       
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
       
        return f"#{r:02x}{g:02x}{b:02x}"

    def setup_ui(self):
        self.window.configure(fg_color=self.colors["bg_primary"])
       
        main_frame = ctk.CTkFrame(self.window, fg_color=self.colors["bg_primary"], corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)
       
        header_frame = ctk.CTkFrame(main_frame, fg_color=self.colors["bg_secondary"], corner_radius=18, height=90)
        header_frame.pack(fill="x", pady=(0, 25))
        header_frame.pack_propagate(False)
       
        header_left = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_left.pack(side="left", fill="y")
       
        
       
        
       
        title_frame = ctk.CTkFrame(header_left, fg_color="transparent")
        title_frame.pack(side="left", padx=(5, 20), pady=20, fill="y")
       
        title_label = ctk.CTkLabel(
            title_frame,
            text="PRISM AI",
            font=("Helvetica", 28, "bold"),
            text_color=self.colors["text_primary"]
        )
        title_label.pack(side="top", anchor="w")
       
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Advanced Voice Assistant",
            font=("Helvetica", 14),
            text_color=self.colors["text_tertiary"]
        )
        subtitle_label.pack(side="top", anchor="w")
       
        personality_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        personality_frame.pack(side="right", padx=20, pady=20)
       
        personality_label = ctk.CTkLabel(
            personality_frame,
            text="AI Personality:",
            font=("Helvetica", 16),
            text_color=self.colors["text_secondary"]
        )
        personality_label.pack(side="left", padx=(0, 15))
       
        self.personality_var = ctk.StringVar(value="College Student")
        personality_menu = ctk.CTkOptionMenu(
            personality_frame,
            values=list(self.model.personalities.keys()),
            variable=self.personality_var,
            command=self.change_personality,
            width=220,
            height=45,
            font=("Helvetica", 15),
            dropdown_font=("Helvetica", 15),
            fg_color=self.colors["accent_primary"],
            button_color=self.colors["accent_primary"],
            button_hover_color=self.colors["accent_tertiary"],
            dropdown_fg_color=self.colors["bg_tertiary"],
            dropdown_hover_color=self.colors["bg_secondary"],
            text_color=self.colors["text_primary"],
            dropdown_text_color=self.colors["text_primary"]
        )
        personality_menu.pack(side="right")
       
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
       
        self.chat_frame = ctk.CTkFrame(
            content_frame,
            fg_color=self.colors["bg_secondary"],
            corner_radius=18,
            border_width=1,
            border_color=self.colors["bg_tertiary"]
        )
        self.chat_frame.pack(fill="both", expand=True, pady=(0, 25))
       
        self.chat_display = ctk.CTkTextbox(
            self.chat_frame,
            font=("Helvetica", 16),
            wrap="word",
            fg_color=self.colors["bg_secondary"],
            text_color=self.colors["text_primary"],
            scrollbar_button_color=self.colors["accent_primary"],
            scrollbar_button_hover_color=self.colors["accent_tertiary"],
            corner_radius=15
        )
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=20)
        self.chat_display.configure(state="disabled")
       
        info_panel = ctk.CTkFrame(
            main_frame,
            fg_color=self.colors["bg_secondary"],
            corner_radius=18,
            height=60,
            border_width=1,
            border_color=self.colors["bg_tertiary"]
        )
        info_panel.pack(fill="x", pady=(0, 25))
        info_panel.pack_propagate(False)
       
        status_frame = ctk.CTkFrame(info_panel, fg_color="transparent")
        status_frame.pack(side="left", padx=20, pady=15)
       
        self.status_indicator = ctk.CTkFrame(
            status_frame,
            width=12,
            height=12,
            corner_radius=6,
            fg_color=self.colors["accent_secondary"]
        )
        self.status_indicator.pack(side="left", padx=(0, 10))
       
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready",
            font=("Helvetica", 15),
            text_color=self.colors["text_secondary"]
        )
        self.status_label.pack(side="left")
       
        language_frame = ctk.CTkFrame(info_panel, fg_color="transparent")
        language_frame.pack(side="right", padx=20, pady=15)
       
        language_icon = ctk.CTkLabel(
            language_frame,
            text="🌐",
            font=("Helvetica", 15),
            text_color=self.colors["text_secondary"]
        )
        language_icon.pack(side="left", padx=(0, 8))
       
        self.language_label = ctk.CTkLabel(
            language_frame,
            text="English",
            font=("Helvetica", 15),
            text_color=self.colors["text_secondary"]
        )
        self.language_label.pack(side="left")
       
        context_frame = ctk.CTkFrame(info_panel, fg_color="transparent")
        context_frame.pack(side="right", padx=20, pady=15)
       
        context_icon = ctk.CTkLabel(
            context_frame,
            text="📝",
            font=("Helvetica", 15),
            text_color=self.colors["text_secondary"]
        )
        context_icon.pack(side="left", padx=(0, 8))
       
        self.context_label = ctk.CTkLabel(
            context_frame,
            text="0 messages",
            font=("Helvetica", 15),
            text_color=self.colors["text_secondary"]
        )
        self.context_label.pack(side="left")
       
        input_container = ctk.CTkFrame(
            main_frame,
            fg_color=self.colors["bg_secondary"],
            corner_radius=30,
            height=70,
            border_width=1,
            border_color=self.colors["bg_tertiary"]
        )
        input_container.pack(fill="x", pady=(0, 15))
        input_container.pack_propagate(False)
       
        input_padding = ctk.CTkFrame(input_container, fg_color="transparent")
        input_padding.pack(fill="both", expand=True, padx=10, pady=10)
       
        self.text_input = ctk.CTkEntry(
            input_padding,
            font=("Helvetica", 16),
            placeholder_text="Type your message here...",
            height=50,
            fg_color=self.colors["bg_tertiary"],
            border_color=self.colors["accent_primary"],
            text_color=self.colors["text_primary"],
            placeholder_text_color=self.colors["text_tertiary"],
            corner_radius=25
        )
        self.text_input.pack(side="left", fill="x", expand=True, padx=(10, 10))
       
        self.text_input.bind("<Return>", lambda event: self.send_text())
       
        self.mic_button = ctk.CTkButton(
            input_padding,
            text="🎤",
            command=self.toggle_listening,
            width=50,
            height=50,
            font=("Helvetica", 20),
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["accent_secondary"],
            corner_radius=25,
            text_color=self.colors["text_primary"],
            border_width=2,
            border_color=self.colors["bg_tertiary"]
        )
        self.mic_button.pack(side="right", padx=(0, 10))
       
        self.send_button = ctk.CTkButton(
            input_padding,
            text="Send",
            command=self.send_text,
            width=100,
            height=50,
            font=("Helvetica", 16, "bold"),
            fg_color=self.colors["accent_primary"],
            hover_color=self.colors["accent_tertiary"],
            corner_radius=25,
            text_color=self.colors["text_primary"]
        )
        self.send_button.pack(side="right", padx=(10, 10))
       
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")
       
        left_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_buttons.pack(side="left")
       
        right_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_buttons.pack(side="right")
       
        self.clear_context_button = self.create_control_button(
            right_buttons,
            "Clear Context",
            "🗑️",
            self.clear_context,
            "right"
        )
       
        self.clear_chat_button = self.create_control_button(
            right_buttons,
            "Clear Chat",
            "✨",
            self.clear_chat,
            "right"
        )

    def create_control_button(self, parent, text, icon, command, side):
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(side=side, padx=5, pady=5)
       
        button = ctk.CTkButton(
            button_frame,
            text=f"{icon} {text}",
            command=command,
            width=160,
            height=45,
            font=("Helvetica", 15),
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["accent_primary"],
            corner_radius=22,
            text_color=self.colors["text_primary"],
            border_width=1,
            border_color=self.colors["bg_tertiary"]
        )
        button.pack()
        return button

    def send_text(self):
        text = self.text_input.get()
        if text.strip():
            self.text_input.delete(0, 'end')
           
            self.status_indicator.configure(fg_color=self.colors["user_msg"])
            self.status_label.configure(text="Processing")
           
            translated_text, detected_lang = self.model.detect_language_and_translate(text)
            self.language_label.configure(text=f"{detected_lang}")
           
            emotion = self.model.detect_emotion(translated_text)
            self.update_chat(text, "user")
           
            context_count = self.model.add_to_history("user", translated_text)
            self.context_label.configure(text=f"{context_count} messages")
           
            threading.Thread(target=self.process_and_respond, args=(translated_text, detected_lang), daemon=True).start()

    def process_and_respond(self, text, detected_lang):
        response = self.model.generate_ai_response(text)
       
        context_count = self.model.add_to_history("assistant", response)
       
        if detected_lang != 'en':
            try:
                response = self.model.translator.translate(response, dest=detected_lang).text
            except Exception as e:
                print(f"Translation error: {str(e)}")
       
        self.window.after(0, lambda: self.update_chat(response, "assistant"))
        self.window.after(0, lambda: self.context_label.configure(text=f"{context_count} messages"))
        self.window.after(0, lambda: self.status_indicator.configure(fg_color=self.colors["accent_secondary"]))
        self.window.after(0, lambda: self.status_label.configure(text="Ready"))

    def change_personality(self, personality):
        old_personality = self.model.current_personality
       
        self.status_indicator.configure(fg_color=self.colors["system_msg"])
        self.status_label.configure(text="Switching")
       
        first_message = self.model.set_personality(personality)
       
        self.update_chat(f"Switched from {old_personality} to {personality}", "system")
        self.context_label.configure(text=f"{self.model.context_count} messages")
        self.update_chat(first_message, "assistant")
       
        self.status_indicator.configure(fg_color=self.colors["accent_secondary"])
        self.status_label.configure(text="Ready")

    def update_chat(self, text, speaker):
        timestamp = time.strftime("%H:%M:%S")
       
        if speaker == "user":
            prefix = "You"
            color = self.colors["user_msg"]
            icon = "👤"
        elif speaker == "assistant":
            prefix = self.model.current_personality
            color = self.colors["assistant_msg"]
            icon = "🤖"
        else:
            prefix = "System"
            color = self.colors["system_msg"]
            icon = "⚙️"
       
        message = f"{icon} [{timestamp}] {prefix}:\n{text}\n\n"
       
        self.chat_display.configure(state="normal")
       
        current_position = self.chat_display.index("end-1c")
        self.chat_display.insert("end", message)
       
        end_position = self.chat_display.index("end-1c")
        message_start = f"{current_position} + 0c"
        message_end = f"{end_position}"
       
        self.chat_display._textbox.tag_add(speaker, message_start, message_end)
        self.chat_display._textbox.tag_config(speaker, foreground=color)
       
        self.chat_display.configure(state="disabled")
       
        self.chat_display.see("end")

    def toggle_listening(self):
        if not self.model.is_listening:
            self.model.is_listening = True
            self.animation_active = True
            self.mic_button.configure(
                text="⏹️",
                fg_color=self.colors["alert"],
                border_color=self.colors["alert"]
            )
            self.status_indicator.configure(fg_color=self.colors["alert"])
            self.status_label.configure(text="Listening")
            threading.Thread(target=self.listen_loop, daemon=True).start()
        else:
            self.model.is_listening = False
            self.animation_active = False
            self.mic_button.configure(
                text="🎙️",
                fg_color=self.colors["bg_tertiary"],
                border_color=self.colors["bg_tertiary"]
            )
            self.status_indicator.configure(fg_color=self.colors["accent_secondary"])
            self.status_label.configure(text="Ready")

    def listen_loop(self):
        while self.model.is_listening:
            text, error = self.model.listen()
           
            if error:
                self.window.after(0, lambda e=error: self.status_label.configure(text=f"{e}"))
                time.sleep(1)
                continue
               
            if text:
                translated_text, detected_lang = self.model.detect_language_and_translate(text)
                self.window.after(0, lambda lang=detected_lang: self.language_label.configure(text=f"{lang}"))
               
                emotion = self.model.detect_emotion(translated_text)
                self.window.after(0, lambda t=text: self.update_chat(t, "user"))
               
                context_count = self.model.add_to_history("user", translated_text)
                self.window.after(0, lambda count=context_count: self.context_label.configure(text=f"{count} messages"))
               
                self.window.after(0, lambda: self.status_indicator.configure(fg_color=self.colors["assistant_msg"]))
                self.window.after(0, lambda: self.status_label.configure(text="Generating"))
               
                response = self.model.generate_ai_response(translated_text)
               
                context_count = self.model.add_to_history("assistant", response)
               
                if detected_lang != 'en':
                    try:
                        response = self.model.translator.translate(response, dest=detected_lang).text
                    except Exception as e:
                        print(f"Translation error: {str(e)}")
               
                self.window.after(0, lambda r=response: self.update_chat(r, "assistant"))
                self.window.after(0, lambda count=context_count: self.context_label.configure(text=f"{count} messages"))
                self.window.after(0, lambda: self.status_indicator.configure(fg_color=self.colors["accent_tertiary"]))
                self.window.after(0, lambda: self.status_label.configure(text="Speaking"))
               
                threading.Thread(target=self.speak_response, args=(response,), daemon=True).start()
               
            time.sleep(0.5)

    def speak_response(self, text):
        success = self.model.speak(text)
        if success:
            self.window.after(0, lambda: self.status_indicator.configure(fg_color=self.colors["accent_secondary"]))
            self.window.after(0, lambda: self.status_label.configure(text="Ready"))
        else:
            self.window.after(0, lambda: self.status_indicator.configure(fg_color=self.colors["alert"]))
            self.window.after(0, lambda: self.status_label.configure(text="Speech Error"))

    def clear_context(self):
        context_count = self.model.clear_context()
        self.context_label.configure(text=f"{context_count} messages")
        self.status_indicator.configure(fg_color=self.colors["system_msg"])
        self.update_chat("Context memory cleared", "system")
        self.window.after(1000, lambda: self.status_indicator.configure(fg_color=self.colors["accent_secondary"]))

    def clear_chat(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self.status_indicator.configure(fg_color=self.colors["system_msg"])
        self.update_chat("Chat cleared", "system")
        self.window.after(1000, lambda: self.status_indicator.configure(fg_color=self.colors["accent_secondary"]))

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = VoiceAssistantUI()
    app.run()
