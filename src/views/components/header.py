import customtkinter as ctk


class Header(ctk.CTkFrame):
    def __init__(
        self,
        master,
        height: int = 60,
        logger=None,
        **kwargs,
    ):
        super().__init__(
            master,
            height=height,
            corner_radius=0,
            fg_color="transparent",
            **kwargs
        )

        self.pack_propagate(False)

        # Title label on the left
        self.title_label = ctk.CTkLabel(self, text="AI Kids Studio Pro")
        self.title_label.pack(side="left", padx=(10, 0))

        # Version label on the right
        self.version_label = ctk.CTkLabel(self, text="v1.0")
        self.version_label.pack(side="right", padx=(0, 10))


__all__ = ["Header"]