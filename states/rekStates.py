from aiogram.dispatcher.filters.state import StatesGroup, State


class AllState(StatesGroup):
    env = State()
    env_remove = State()


class DelState(StatesGroup):
    del_user = State()


class TugmaData(StatesGroup):
    tugma_plus = State()
    tugma_minus = State()


class RekData(StatesGroup):
    find_winner = State()
    new_project = State()
    for_winner_score = State()
    gift_for_winner = State()
    gift_for_winner_link = State()
    gift_for_winner_post = State()
    first_gift = State()
    req_text = State()
    add_list_plus_channel = State()
    required_subscribe = State()
    add_list_minus = State()
    add_list_plus = State()
    add_list_minus_channel = State()
    start = State()
    number_phone = State()
    delete_secret = State()
    add_secret = State()
    check = State()
    score_0 = State()
    after_sub = State()
    url = State()
    limit = State()
    main_content = State()
    main_content_2 = State()
    to_winners = State()
    choice = State()
    special = State()
    picture = State()
    score = State()
    text = State()
    shart = State()
    channel_id = State()
    add = State()
    delete = State()
    kbsh = State()
    winners = State()


class Number(StatesGroup):
    number = State()
    name = State()
    username = State()
    add_user = State()


class DelUser(StatesGroup):
    user = State()
    fix = State()


class Lesson(StatesGroup):
    choice_section = State()
    choice_button = State()
    les_del = State()
    choice_video_section = State()
    choice_photo_section = State()
    choice_audio_section = State()
    add_audio = State()
    add_audio_text = State()
    add_video = State()
    add_video_text = State()
    add_image = State()
    add_image_text = State()
    dell = State()
    but_add = State()
    but_del = State()


class TestData(StatesGroup):
    # Test Creation States
    test_code = State()
    test_name = State()
    test_questions_count = State()
    test_correct_answers = State()
    
    # Test Taking States
    test_answer_input = State()
    
    # Test Management States
    test_edit_select = State()
    test_edit_field = State()
    test_delete_confirm = State()
