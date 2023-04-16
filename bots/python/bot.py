import aiohttp
import api


class Bot:
    def __init__(self, session: aiohttp.ClientSession, name: str, bot_id: str):
        self.session = session
        self.name = name
        self.bot_id = bot_id
        self.color = None
        self.x = None
        self.y = None
        # The colour of the pixel the bot is on
        self.pixel_color = None

    def __set_position_and_pixel_color(self, response):
        self.x = response['x']
        self.y = response['y']
        self.pixel_color = response['color']

    async def set_color(self, color: int):
        """
        Sets the color of the bot. This determines in what color the bot will paint in.

        :param color:
        :return:
        """
        self.color = color

        response = await api.set_color(self.session, self.bot_id, color)
        self.__set_position_and_pixel_color(response)

        return self

    async def paint_pixel(self):
        response = await api.paint_pixel(self.session, self.bot_id)

        self.__set_position_and_pixel_color(response)

        return self

    async def clear_pixel(self):
        await api.clear_pixel(self.session, self.bot_id)

        # Clear pixel does not return position or color
        # Current pixel will be removed on the server, so its color will be set to None here
        self.pixel_color = None

        return self

    async def say(self, msg: str):
        response = await api.say(self.session, self.bot_id, msg)

        self.__set_position_and_pixel_color(response)

        return self

    async def move_bot(self, direction: str, dist: int):
        response = None
        for i in range(dist):
            response = await api.move_bot(self.session, self.bot_id, direction)

        self.__set_position_and_pixel_color(response)

        return self

    async def look(self):
        response = await api.look(self.session, self.bot_id)

        # Returns the ASCII representation of the current canvas
        return response

    # !! Add your own drawing functions here !!

    async def draw_rectangle(self, width: int):
        """
        Example helper function for drawing a simple rectangle using the api calls
        Here, we are moving the bot first to a certain direction and then painting a
        single pixel with a color that was previously set in the main function for the bot.

        :param width:
        :return:
        """
        dirs = ["RIGHT", "DOWN", "LEFT", "UP"]

        for direction in dirs:
            for i in range(width):
                # Move bot and paint a pixel one pixel at time
                await api.move_bot(self.session, self.bot_id, direction)
                await self.paint_pixel()

        return self
