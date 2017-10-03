from model_mommy import mommy
from model_mommy.recipe import Recipe, seq, foreign_key

from talentmap_api.user_profile.models import UserProfile
from talentmap_api.position.models import Position, Grade, Skill, Classification
from talentmap_api.organization.tests.mommy_recipes import post, orphaned_organization

grade = Recipe(
    Grade,
    code=seq("")
)

skill = Recipe(
    Skill,
    code=seq("")
)

position = Recipe(
    Position,
    grade=foreign_key('grade'),
    skill=foreign_key('skill'),
    post=foreign_key(post),
    bureau=foreign_key(orphaned_organization)
)


def favorite_position():
    pos = mommy.make(Position)
    pos.classifications.add(mommy.make(Classification))
    up = UserProfile.objects.last()
    up.favorite_positions.add(pos)
    up.save()
    return pos


def highlighted_position():
    pos = mommy.make(Position)
    org = mommy.make("organization.Organization")
    org.highlighted_positions.add(pos)
    return pos
