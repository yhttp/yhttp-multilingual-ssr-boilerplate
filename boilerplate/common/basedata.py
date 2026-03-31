from . import models


CITIES = [
    ('Muscat', 'مسقط', 'مسقط'),
    ('Salalah', 'صلاله', 'صلالة'),
    ('Seeb', 'سیب', 'السيب'),
    ('Sohar', 'صحار', 'صحار'),
    ('Nizwa', 'نزوی', 'نزوى'),
    ('Sur', 'صور', 'صور'),
    ('Ibri', 'عبری', 'عبري'),
    ('Rustaq', 'رستاق', 'الرستاق'),
    ('Buraimi', 'البریمی', 'البريمي'),
    ('Khasab', 'خصب', 'خصب'),
    ('Barka', 'برکاء', 'بركاء'),
    ('Duqm', 'دقم', 'الدقم'),
    ('Ibra', 'ابراء', 'إبراء'),
    ('Bahla', 'بهلاء', 'بهلاء'),
    ('Saham', 'صحم', 'صحم'),
    ('Shinas', 'شناص', 'شناص'),
    ('Liwa', 'لوی', 'لوى'),
    ('Izki', 'ازکی', 'إزكي'),
    ('Samail', 'سمائل', 'سمائل'),
    ('Adam', 'ادم', 'أدم')
]


def insert(db):
    print('generating common module\'s base data')
    with db.session() as session:
        for (en, fa, ar) in CITIES:
            print(f'Creating city: {en}')
            member = models.City(
                title_en=en,
                title_fa=fa,
                title_ar=ar,
            )

            session.add(member)
            session.commit()
