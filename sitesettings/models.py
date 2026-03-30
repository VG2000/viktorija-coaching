from django.db import models

from wagtail.admin.panels import MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting
class SiteSettings(BaseSiteSetting):
    """Global site settings editable in Wagtail admin."""

    site_name = models.CharField(max_length=255, default="Viktorija Coaching")
    tagline = models.CharField(max_length=255, blank=True)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Site logo",
    )
    favicon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Favicon (recommended: 32x32 PNG)",
    )

    # Contact
    contact_email = models.EmailField(blank=True)

    # Social
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # Footer
    footer_text = models.TextField(blank=True)
    copyright_name = models.CharField(
        max_length=255, blank=True, default="Viktorija Coaching"
    )

    panels = [
        MultiFieldPanel(
            ["site_name", "tagline", "logo", "favicon"],
            heading="Branding",
        ),
        MultiFieldPanel(
            ["contact_email"],
            heading="Contact",
        ),
        MultiFieldPanel(
            ["instagram_url", "facebook_url", "linkedin_url"],
            heading="Social Media",
        ),
        MultiFieldPanel(
            ["footer_text", "copyright_name"],
            heading="Footer",
        ),
    ]

    class Meta:
        verbose_name = "Site Settings"
