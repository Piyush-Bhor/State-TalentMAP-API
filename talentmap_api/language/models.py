from django.db import models
from djchoices import DjangoChoices, ChoiceItem

import logging

from talentmap_api.common.models import StaticRepresentationModel


class Language(StaticRepresentationModel):
    '''
    The language model represents an individual language, such as English, French, et. al.
    It is typically linked together with a language proficiency to create a qualification,
    but is maintained as a separate model to facilitate filtering and logical separations.
    '''

    code = models.TextField(db_index=True, unique=True, null=False, help_text="The code representation of the language")
    long_description = models.TextField(null=False, help_text="Long-format description of the language, typically the name")
    short_description = models.TextField(null=False, help_text="Short-format description of the language, typically the name")
    effective_date = models.DateField(null=False, help_text="The date after which the language is in effect")

    def __str__(self):
        return f"{self.long_description} ({self.code})"

    class Meta:
        managed = True
        ordering = ["code"]


class Proficiency(StaticRepresentationModel):
    '''
    The language proficiency represents a positions linguistic proficiency requirement,
    or the linguistic proficiency of an individual. These are typically not used as
    stand-alone instances, but are linked via the Language qualification model with
    a specific language.

    Possible values: 0, 0+, 1, 1+, 2, 2+, 3, 3+, 4, 4+, 5; which represent increasing
                     levels of fluency with a language
                     F - for a "failed" state on a proficiency exam
                     P - for a "passed" state on a proficiency exam
                     X - for a "not taken" state on a proficiency exam
    '''

    code = models.TextField(null=False, unique=True, help_text="The code representing the linguistic proficiency")
    description = models.TextField(null=False, help_text="Text describing the level of proficiency")

    # The ordered ranking of proficiencies for greater than/less than comparisons
    RANKING = ["F", "X", "P", "0", "0+", "1", "1+", "2", "2+", "3", "3+", "4", "4+", "5"]

    def __str__(self):
        return f"{self.code}"

    class Meta:
        managed = True
        ordering = ["code"]


class Qualification(StaticRepresentationModel):
    '''
    The language qualification is defined by a combination of language proficiencies
    and a specific language. For example, German 2/2+, where the first numeral denotes
    the reading/writing proficiency, and the second numeral denotes the speaking/listening
    proficiency.
    '''

    language = models.ForeignKey('Language', on_delete=models.PROTECT, null=False, related_name='qualifications')
    reading_proficiency = models.ForeignKey('Proficiency', on_delete=models.PROTECT, null=False, related_name='reading_qualifications')
    spoken_proficiency = models.ForeignKey('Proficiency', on_delete=models.PROTECT, null=False, related_name='spoken_qualifications')

    @staticmethod
    def get_or_create_by_codes(language_code, reading_proficiency_code, spoken_proficiency_code):
        '''
        Gets or creates a language qualification using the language and proficiency codes.

        Args:
            language_code (str) - The language's code, for example "FR" for French
            reading_proficiency_code (str) - The written proficiency's code, for example "2+"
            spoken_proficiency_code (str) - The spoken proficiency's code, for example "2+"

        Returns:
            obj: The qualification object
            bool: Whether the object was created or found
        '''
        language = Language.objects.filter(code=language_code)
        reading_proficiency = Proficiency.objects.filter(code=reading_proficiency_code)
        spoken_proficiency = Proficiency.objects.filter(code=spoken_proficiency_code)

        if language.count() != 1 or reading_proficiency.count() != 1 or spoken_proficiency.count() != 1:
            logging.getLogger('console').warn(f"Tried to create language qualification, but failed: {language_code} ({language.count()}) {reading_proficiency_code} ({reading_proficiency.count()}) {spoken_proficiency_code} ({spoken_proficiency.count()})")
            return None, False

        return Qualification.objects.get_or_create(language=language.first(), reading_proficiency=reading_proficiency.first(), spoken_proficiency=spoken_proficiency.first())

    def __str__(self):
        return f"{self.language} {self.reading_proficiency}/{self.spoken_proficiency}"

    class Meta:
        managed = True
        ordering = ["language__code"]
        unique_together = (('language', 'reading_proficiency', 'spoken_proficiency'))


class Waiver(StaticRepresentationModel):
    '''
    The waiver model represents a language requirement waiver for a particular position
    assignment, along with the status
    '''

    class Type(DjangoChoices):
        partial = ChoiceItem("partial")
        full = ChoiceItem("full")

    class Status(DjangoChoices):
        approved = ChoiceItem("approved")
        requested = ChoiceItem("requested")
        denied = ChoiceItem("denied")

    type = models.TextField(default=Type.full, choices=Type.choices)
    status = models.TextField(default=Status.requested, choices=Status.choices)

    user = models.ForeignKey("user_profile.UserProfile", on_delete=models.CASCADE, related_name="language_waivers")
    position = models.ForeignKey("position.Position", related_name="language_waivers")
    bidcycle = models.ForeignKey("bidding.BidCycle", related_name="language_waivers")
    language = models.ForeignKey("language.Language", related_name="waivers")

    request_date = models.DateField(auto_now_add=True)
    decision_date = models.DateField(null=True)

    class Meta:
        managed = True
        ordering = ["request_date"]
