import customtkinter as ctk


class StatusBar(ctk.CTkFrame):
    def __init__(
        self,
        master,
        height: int = 30,
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

        self._status_label = ctk.CTkLabel(self, text="Ready")
        self._status_label.pack(side="left", padx=10, pady=5)

    def set_status(self, text: str) -> None:
        self._status_label.configure(text=text)


__all__ = ["StatusBar"]