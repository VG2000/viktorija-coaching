from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks


class HomePage(Page):
    """Landing page with modular sections."""

    max_count = 1

    # Hero Section
    hero_title = models.CharField(max_length=255)
    hero_subtitle = models.CharField(max_length=500, blank=True)
    hero_cta_text = models.CharField(max_length=100, default="Work With Me")
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # About Preview Section
    about_heading = models.CharField(max_length=255, blank=True)
    about_text = RichTextField(blank=True)
    about_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Services Preview
    services_heading = models.CharField(max_length=255, default="How I Can Help")
    services_subheading = models.TextField(blank=True)
    services_items = StreamField(
        [
            (
                "service",
                blocks.StructBlock(
                    [
                        (
                            "icon",
                            blocks.CharBlock(
                                required=False, help_text="Emoji or icon name"
                            ),
                        ),
                        ("title", blocks.CharBlock()),
                        ("description", blocks.TextBlock()),
                    ]
                ),
            )
        ],
        blank=True,
    )

    # Testimonials Section
    testimonials_heading = models.CharField(
        max_length=255, default="What Clients Say"
    )
    featured_testimonials = StreamField(
        [
            (
                "testimonial",
                blocks.StructBlock(
                    [
                        ("quote", blocks.TextBlock()),
                        ("author_name", blocks.CharBlock()),
                        ("author_title", blocks.CharBlock(required=False)),
                        ("author_image", ImageChooserBlock(required=False)),
                    ]
                ),
            )
        ],
        blank=True,
    )

    # Newsletter Section
    newsletter_heading = models.CharField(
        max_length=255, default="Join My Community"
    )
    newsletter_text = models.TextField(blank=True)

    # Bottom CTA
    cta_heading = models.CharField(max_length=255, blank=True)
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
                "hero_title",
                "hero_subtitle",
                "hero_cta_text",
                "hero_cta_link",
                "hero_image",
            ],
            heading="Hero Section",
        ),
        MultiFieldPanel(
            [
                "about_heading",
                "about_text",
                "about_image",
            ],
            heading="About Preview",
        ),
        MultiFieldPanel(
            [
                "services_heading",
                "services_subheading",
                "services_items",
            ],
            heading="Services Preview",
        ),
        MultiFieldPanel(
            [
                "testimonials_heading",
                "featured_testimonials",
            ],
            heading="Testimonials",
        ),
        MultiFieldPanel(
            [
                "newsletter_heading",
                "newsletter_text",
            ],
            heading="Newsletter",
        ),
        MultiFieldPanel(
            [
                "cta_heading",
                "cta_text",
                "cta_button_text",
                "cta_button_link",
            ],
            heading="Bottom CTA",
        ),
    ]

    class Meta:
        verbose_name = "Home Page"
