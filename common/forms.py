from django import forms

TAILWIND_INPUT = (
    "w-full rounded-md border-gray-300 shadow-sm "
    "focus:border-indigo-500 focus:ring-indigo-500 p-2"
)

TAILWIND_SELECT = TAILWIND_INPUT
TAILWIND_TEXTAREA = TAILWIND_INPUT
TAILWIND_CHECKBOX = "rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"


class TailwindFormMixin:
    """
    Automatically apply Tailwind CSS classes to all form fields.
    """

    def _apply_tailwind_classes(self):
        for field in self.fields.values():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", TAILWIND_CHECKBOX)

            elif isinstance(
                widget,
                (
                    forms.TextInput,
                    forms.EmailInput,
                    forms.NumberInput,
                    forms.Select,
                    forms.Textarea,
                    forms.ClearableFileInput,
                ),
            ):
                widget.attrs.setdefault("class", TAILWIND_INPUT)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_tailwind_classes()


class TailwindModelForm(TailwindFormMixin, forms.ModelForm):
    pass
