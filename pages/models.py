from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks


class AboutPage(Page):
    """About/Bio page."""

    max_count = 1
    parent_page_types = ["home.HomePage"]

    # Hero Section
    hero_heading = models.CharField(max_length=255, default="Hi, I'm Viktorija")
    hero_subheading = models.TextField(blank=True)
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Story Section
    story = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            (
                "image_text_block",
                blocks.StructBlock(
                    [
                        ("image", ImageChooserBlock()),
                        (
                            "image_position",
                            blocks.ChoiceBlock(
                                choices=[
                                    ("left", "Image Left"),
                                    ("right", "Image Right"),
                                ]
                            ),
                        ),
                        ("text", blocks.RichTextBlock()),
                    ]
                ),
            ),
            ("quote", blocks.BlockQuoteBlock()),
        ],
        blank=True,
    )

    # Credentials/Certifications
    credentials_heading = models.CharField(
        max_length=255, default="Credentials & Training"
    )
    credentials = StreamField(
        [
            (
                "credential",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock()),
                        ("organization", blocks.CharBlock(required=False)),
                        ("year", blocks.CharBlock(required=False)),
                        ("logo", ImageChooserBlock(required=False)),
                    ]
                ),
            )
        ],
        blank=True,
    )

    # Values/Philosophy
    philosophy_heading = models.CharField(max_length=255, default="My Approach")
    philosophy_text = RichTextField(blank=True)

    # Fun Facts / Personal Section
    personal_heading = models.CharField(max_length=255, default="Beyond the Bio")
    personal_facts = StreamField(
        [
            (
                "fact",
                blocks.StructBlock(
                    [
                        ("emoji", blocks.CharBlock(max_length=10, required=False)),
                        ("text", blocks.CharBlock()),
                    ]
                ),
            )
        ],
        blank=True,
    )

    # CTA
    cta_heading = models.CharField(
        max_length=255, default="Ready to Start Your Journey?"
    )
    cta_text = models.TextField(blank=True)
    cta_button_text = models.CharField(max_length=100, default="Let's Connect")
    cta_button_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                "hero_heading",
                "hero_subheading",
                "hero_image",
            ],
            heading="Hero Section",
        ),
        "story",
        MultiFieldPanel(
            [
                "credentials_heading",
                "credentials",
            ],
            heading="Credentials",
        ),
        MultiFieldPanel(
            [
                "philosophy_heading",
                "philosophy_text",
            ],
            heading="Philosophy",
        ),
        MultiFieldPanel(
            [
                "personal_heading",
                "personal_facts",
            ],
            heading="Personal Touch",
        ),
        MultiFieldPanel(
            [
                "cta_heading",
                "cta_text",
                "cta_button_text",
                "cta_button_link",
            ],
            heading="Call to Action",
        ),
    ]

    class Meta:
        verbose_name = "About Page"
