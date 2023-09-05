from ninja import NinjaAPI

api = NinjaAPI()


@api.get("/")
def test(request):
    return {"result": True}
