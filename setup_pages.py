import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'viktorijacoaching.settings.dev'))
django.setup()

from wagtail.models import Page, Site
from home.models import HomePage, HomePage2
from pages.models import AboutPage

root = Page.objects.get(depth=1)

if not HomePage.objects.exists():
    welcome = Page.objects.filter(depth=2).first()
    if welcome:
        welcome.delete()
        root = Page.objects.get(depth=1)
    hp = HomePage(
        title='Home', slug='home',
        hero_title='Transform Your Life with Purpose & Clarity',
        hero_subtitle='Empowering ambitious women to unlock their full potential through personalized coaching, mindset mastery, and strategic action.',
        hero_cta_text='Work With Me',
        about_heading='Meet Viktorija',
        about_text='<p>I am a certified life coach passionate about helping women step into their power, find clarity in their vision, and build lives that truly light them up. With a background in psychology and years of coaching experience, I bring a unique blend of warmth, insight, and practical strategy to every session.</p>',
        services_heading='How I Can Help',
        services_subheading='Whether you are navigating a career transition, seeking deeper self-awareness, or ready to level up in every area of life, I have a path designed for you.',
        testimonials_heading='What Clients Say',
        newsletter_heading='Join My Community',
        newsletter_text='Get weekly insights on personal growth, mindset shifts, and practical tools delivered straight to your inbox.',
        cta_heading='Ready to Begin Your Transformation?',
        cta_text='Every journey starts with a single step. Book a free discovery call and let us explore how coaching can help you create the life you have been dreaming of.',
        cta_button_text="Let's Connect",
    )
    root.add_child(instance=hp)
    hp.save_revision().publish()
    print("Created HomePage")
else:
    hp = HomePage.objects.first()
    print("HomePage exists")

site = Site.objects.first()
if site:
    site.root_page = hp
    site.site_name = 'Viktorija Coaching'
    site.save()
else:
    Site.objects.create(hostname='localhost', root_page=hp, is_default_site=True, site_name='Viktorija Coaching')

if not AboutPage.objects.exists():
    about = AboutPage(
        title='About', slug='about', show_in_menus=True,
        hero_heading="Hi, I'm Viktorija",
        hero_subheading='Life coach, mindset mentor, and your biggest cheerleader on the path to becoming who you were always meant to be.',
        credentials_heading='Credentials & Training',
        philosophy_heading='My Approach',
        philosophy_text='<p>I believe that every woman has the power within her to create extraordinary change. My coaching approach blends evidence-based psychology with intuitive guidance, creating a safe space for deep transformation.</p>',
        personal_heading='Beyond the Bio',
        cta_heading='Ready to Start Your Journey?',
        cta_text='I would love to hear your story and explore how we can work together.',
        cta_button_text="Let's Connect",
    )
    hp.add_child(instance=about)
    about.save_revision().publish()
    print("Created AboutPage")
else:
    print("AboutPage exists")

if not HomePage2.objects.exists():
    hp2 = HomePage2(
        title='Homepage 2', slug='home-2', show_in_menus=True,
        hero_heading='Your Journey Starts Here',
        hero_text='Embody your truth and confidently step into the life you were meant to live. Through personalized coaching, we will uncover what is holding you back and create a clear path forward.',
        hero_cta_text='Book a Discovery Call',
        services_heading='How I Can Help',
        about_heading='Meet Viktorija',
        about_text='<p>With over a decade of experience in coaching and a background in psychology, I have dedicated my life to helping women reconnect with their authentic selves.</p><p>My approach is rooted in the belief that transformation happens not through force, but through gentle, honest exploration of who we truly are beneath the layers of expectation and conditioning.</p>',
        about_cta_text='Learn More',
        cta_heading='Ready to Begin?',
        cta_text='Take the first step toward living with more clarity, confidence, and purpose. Book a complimentary discovery call and let us explore what is possible together.',
        cta_button_text='Book a Discovery Call',
    )
    hp.add_child(instance=hp2)
    hp2.save_revision().publish()
    print("Created HomePage2")
else:
    print("HomePage2 exists")

for p in Page.objects.all():
    print(f"  {p.depth} | {p.title} | {type(p.specific).__name__}")
