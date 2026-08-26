from dataclasses import dataclass


# The client name and avatar are set when creating the Discord application.
# If you use my CLIENT_ID, it will default to "Difference" and my av.
@dataclass
class client_discord_tokens:
    CLIENT_ID: str = "1522675721246478536"
    CLIENT_PUBLIC_KEY: str = "983e95a6eb09f546b0f5c9264310861af65d5ef9d6488c64e1e49d06384dc160"
