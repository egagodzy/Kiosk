from db.tables.users import users
from db.tables.cookie import cookie
from db.tables.pages import pages
from db.tables.main_page import main_page
from db.config import database
import string
import random
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import aiofiles
import aiofiles.os
from pathlib import Path
from starlette.requests import Request
import shutil
from typing import List
import os


class GetUser(BaseModel):
    username: str
    userpassword: str
    

class GetToken(BaseModel):
    token: str
    

class GetPageId(BaseModel):
    id: int
    

class GetPageName(BaseModel):
    pagename: str
    

class CreatePage(BaseModel):
    pagename: str
    pagetype: str
    pageicon: str
    pagetitle: str
    pagebody: str
    pagenav: str
    pagesrc: str
    

class ChangePage(BaseModel):
    pageid: int
    pagename: str
    pagetype: str
    pageicon: str
    pagetitle: str
    pagebody: str
    pagenav: str
    pagesrc: str
    

class ChangeMainPage(BaseModel):
    pagename: str
    

class ChangePageDir(BaseModel):
    cureent_pagename: str
    new_pagename: str


class DeleteVideo(BaseModel):
    videosrc: str
    

class DeletePDF(BaseModel):
    pdfsrc: str
    

class DeleteIMGs(BaseModel):
    pagename: str
    imgsrc: list
    

class IconData(BaseModel):
    iconsrc: str
    
class DelPage(BaseModel):
    pagename: str


class SaveFile(BaseModel):
    files: bytes



app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/login/")
async def login(user: GetUser):
    query = users.select().where(users.c.username == user.username)
    get_user = await database.fetch_one(query)
    if get_user == None:
        return {"Auth": 1}
    else:
        if get_user.userpassword == user.userpassword:
            test = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            testquery = cookie.insert().values(usercookie=test, username=get_user.username)
            await database.execute(testquery)
            return {"Auth": test}
        else:
            return {"Auth": 2}


@app.post("/check_user/")
async def check_user(token: GetToken):
    print(token)
    query = cookie.select().where(cookie.c.usercookie == token.token)
    get_username = await database.fetch_one(query)
    if get_username == None:
        return {"Check": "Fail"}
    else:
        print(get_username.username)
        query2 = users.select().where(users.c.username == get_username.username)
        get_user_data = await database.fetch_one(query2)
        return get_user_data


@app.get("/get_all_pages/")
async def get_all_pages():
    query = pages.select()
    get_pages = await database.fetch_all(query)
    return get_pages


@app.post("/get_page_by_id/")
async def get_page_by_id(id: GetPageId):
    print(id.id)
    query = pages.select().where(pages.c.id==id.id)
    get_data_page = await database.fetch_one(query)
    print(get_data_page)
    return {"Page": get_data_page}


@app.post("/get_page_by_name/")
async def get_page_by_name(name: GetPageName):
    print(name)
    query = pages.select().where(pages.c.pagename==name.pagename)
    get_data_page = await database.fetch_one(query)
    print(get_data_page)
    return {"Page": get_data_page}


@app.post("/get_pagename/")
async def get_pagename(pagename: GetPageName):
    print(pagename)
    query = pages.select().where(pages.c.pagename==pagename.pagename)
    get_page_name = await database.fetch_one(query)
    if get_page_name is None:
        return {"status": 1}
    else:
        return {"status": 2}
    

@app.post("/create_page/")
async def create_page(page: CreatePage):
    print(page)
    query = pages.insert().values(pagename=page.pagename,
                                  pagetype=page.pagetype,
                                  pageicon=page.pageicon,
                                  pagetitle=page.pagetitle,
                                  pagebody=page.pagebody,
                                  pagenav=page.pagenav,
                                  pagesrc=page.pagesrc)
    await database.execute(query)
    return {"status": "Успешно"}


@app.post("/change_page/")
async def change_page(page: ChangePage):
    print(page)
    query = pages.update().where(pages.c.id == page.pageid).values(pagename=page.pagename,
                                                                   pagetype=page.pagetype,
                                                                   pageicon=page.pageicon,
                                                                   pagetitle=page.pagetitle,
                                                                   pagebody=page.pagebody,
                                                                   pagenav=page.pagenav,
                                                                   pagesrc=page.pagesrc)
    await database.execute(query)
    return {"status": "Успешно"}


@app.post("/change_page_dir/")
async def change_page_dir(pagename: ChangePageDir):
    print(pagename.cureent_pagename)
    print(pagename.new_pagename)
    query = pages.select().where(pages.c.pagename == pagename.cureent_pagename)
    get_page = await database.fetch_one(query)
    print(get_page)
    if get_page.pagetype == 'Images':
        parent_dir = f"{Path.cwd()}/Front/public/"
        directory_img = "img/"
        path_img = f"{parent_dir}{directory_img}"
        current_path_dir_page = f"{path_img}{pagename.cureent_pagename}"
        new_path_dir_page = f"{path_img}{pagename.new_pagename}"
        shutil.copytree(current_path_dir_page, new_path_dir_page)
        shutil.rmtree(current_path_dir_page)
        #print(f'EtoGetPage: {get_page.pagesrc.replace(pagename.cureent_pagename, pagename.new_pagename)}')
        #print(f"ETO PAGEICON: {get_page.pageicon}")
        if get_page.pageicon == '':
            return {"ChangedSRC": get_page.pagesrc.replace(pagename.cureent_pagename, pagename.new_pagename)}
        else:
            return {"ChangedSRC": get_page.pagesrc.replace(pagename.cureent_pagename, pagename.new_pagename), "ChangedIconSRC": get_page.pageicon.replace(pagename.cureent_pagename, pagename.new_pagename)}
    elif get_page.pagetype == 'Video':
        parent_dir = f"{Path.cwd()}/Front/public/"
        directory_vid = "video/"
        path_vid = f"{parent_dir}{directory_vid}"
        current_path_dir_page = f"{path_vid}{pagename.cureent_pagename}"
        new_path_dir_page = f"{path_vid}{pagename.new_pagename}"
        shutil.copytree(current_path_dir_page, new_path_dir_page)
        shutil.rmtree(current_path_dir_page)
        #print(f'EtoGetPage: {get_page.pagesrc.replace(pagename.cureent_pagename, pagename.new_pagename)}')
        #print(f"ETO PAGEICON: {get_page.pageicon}")
        if get_page.pageicon == '':
            return {"ChangedSRC": get_page.pagesrc.replace(pagename.cureent_pagename, pagename.new_pagename)}
        else:
            return {"ChangedSRC": get_page.pagesrc.replace(pagename.cureent_pagename, pagename.new_pagename), "ChangedIconSRC": get_page.pageicon.replace(pagename.cureent_pagename, pagename.new_pagename)}
    elif get_page.pagetype == 'PDF':
        parent_dir = f"{Path.cwd()}/Front/public/"
        directory_pdf = "pdf/"
        path_pdf = f"{parent_dir}{directory_pdf}"
        current_path_dir_page = f"{path_pdf}{pagename.cureent_pagename}"
        new_path_dir_page = f"{path_pdf}{pagename.new_pagename}"
        shutil.copytree(current_path_dir_page, new_path_dir_page)
        shutil.rmtree(current_path_dir_page)
        #print(f'EtoGetPage: {get_page.pagesrc.replace(pagename.cureent_pagename, pagename.new_pagename)}')
        #print(f"ETO PAGEICON: {get_page.pageicon}")
        if get_page.pageicon == '':
            return {"ChangedSRC": get_page.pagesrc.replace(pagename.cureent_pagename, pagename.new_pagename)}
        else:
            return {"ChangedSRC": get_page.pagesrc.replace(pagename.cureent_pagename, pagename.new_pagename), "ChangedIconSRC": get_page.pageicon.replace(pagename.cureent_pagename, pagename.new_pagename)}
    elif get_page.pagetype == 'SimplePage':
        parent_dir = f"{Path.cwd()}/Front/public/"
        directory_sp = "simplepage/"
        path_sp = f"{parent_dir}{directory_sp}"
        current_path_dir_page = f"{path_sp}{pagename.cureent_pagename}"
        new_path_dir_page = f"{path_sp}{pagename.new_pagename}"
        shutil.copytree(current_path_dir_page, new_path_dir_page)
        shutil.rmtree(current_path_dir_page)
        return {"ChangedIconSRC": get_page.pageicon.replace(pagename.cureent_pagename, pagename.new_pagename)}
        

@app.post("/change_main_page/")
async def change_main_page(page: ChangeMainPage):
    print(page)
    query = main_page.select().where(main_page.c.id == 1)
    take_main_page = await database.fetch_one(query)
    print(take_main_page)
    if take_main_page == None:
        newquery = main_page.insert().values(pagename=page.pagename)
        await database.execute(newquery)
        return {"status": "Главная страница успешно создана"}
    else:
        supernewquery = main_page.update().where(main_page.c.id == 1).values(pagename=page.pagename)
        await database.execute(supernewquery)
        return {"status": "Главная страница успешно обновлена"}


@app.get("/get_main_page")
async def get_main_page():
    query = main_page.select().where(main_page.c.id == 1)
    take_main_page = await database.fetch_one(query)
    return take_main_page


@app.post("/multi-file/")
async def create_files(request: Request):
    get_files = {}
    get_page_name = {}
    async with request.form() as form:
        for i in form:
            try:
                filename = form[i].filename
                filetype = form[i].content_type
                filefile = form[i].file.read()
                get_files[i] = {'filename': filename, 'filetype': filetype, 'filedata': filefile}
            except:
                pagename = form[i]
                get_page_name["pagename"] = pagename
    parent_dir = f"{Path.cwd()}/Front/public/"
    directory_img = "img/"
    path_img = f"{parent_dir}{directory_img}"
    path_dir_page = ''
    for dora, dura in get_page_name.items():
        path_dir_page = f"{path_img}{dura}"
        #print(f'Папка ИМГ создана?\nОтвет: {path.exists(path_img)}')
        if await aiofiles.os.path.exists(path_img) == True:
            print("Папка IMG уже создана")
            if await aiofiles.os.path.exists(path_dir_page) == True:
                print("Папка c названием уже страницы создана")
                for key, value in get_files.items():
                    async with aiofiles.open(f"{path_dir_page}/{value['filename']}", 'wb') as out_file:
                        content = value['filedata']
                        await out_file.write(content)
            else: 
                await aiofiles.os.mkdir(path_dir_page)
                print(f"Папка {dura} уже страницы создана")
                for key, value in get_files.items():
                    async with aiofiles.open(f"{path_dir_page}/{value['filename']}", 'wb') as out_file:
                        content = value['filedata']
                        await out_file.write(content)
        else:
            await aiofiles.os.mkdir(path_img)
            print("Папка IMG успешно создана")
            if await aiofiles.os.path.exists(path_dir_page) == True:
                print("Папка c названием уже страницы создана")
                for key, value in get_files.items():
                    async with aiofiles.open(f"{path_dir_page}/{value['filename']}", 'wb') as out_file:
                        content = value['filedata']
                        await out_file.write(content)
            else: 
                await aiofiles.os.mkdir(path_dir_page)
                print(f"Папка {dura} уже страницы создана")
                for key, value in get_files.items():
                    async with aiofiles.open(f"{path_dir_page}/{value['filename']}", 'wb') as out_file:
                        content = value['filedata']
                        await out_file.write(content)
    print(dura)
    newquery = pages.select().where(pages.c.pagename == dura)
    dataL = await database.fetch_one(newquery)
    print(dataL)
    if dataL is None:
        return {"NewSRC": "Пока пусто."}
    else:
        return {"NewSRC": dataL.pagesrc}
    #    try:
    #        os.mkdir(path_img)
    #        print("Папка img создана")
    #        try:
    #            await aiofiles.os.mkdir(path_dir_page) 
    #            #os.mkdir(path_dir_page)
    #            print("Папка c названием страницы создана")
    #        except OSError as error:
    #            print("Папка c названием уже доступна")
    #    except OSError as error:
    #        print("Папка img уже доступна")
    #        try: 
    #            os.mkdir(path_dir_page)
    #            print("Папка c названием страницы создана")
    #            for key, value in get_files.items():
    #                async with aiofiles.open(f"{path_dir_page}/{value['filename']}", 'wb') as out_file:
    #                    content = value['filedata']
    #                    await out_file.write(content)
    #        except OSError as error:
    #            print("Папка c названием уже доступна")
    
    
@app.post("/single-file/")
async def create_file(files: List[UploadFile] = File(), pagename: str = Form()):
    #print(files)
    print(pagename)
    directory_vid = "video/"
    directory_pdf = "pdf/"
    parent_dir = f"{Path.cwd()}/Front/public/"
    path_vid = f"{parent_dir}{directory_vid}"
    path_pdf = f"{parent_dir}{directory_pdf}"
    for file in files:
        if file.content_type == 'video/mp4':
            path_dir_page = f"{path_vid}{pagename}"
            if await aiofiles.os.path.exists(path_vid) == True:
                print("Папка video уже доступна")
                if await aiofiles.os.path.exists(path_dir_page) == True:
                    print(f"Папка {pagename} уже доступна")
                    async with aiofiles.open(f'{path_dir_page}/{file.filename}', 'wb') as out_file:
                        content = file.file.read()
                        await out_file.write(content)
                else: 
                    await aiofiles.os.mkdir(path_dir_page)
                    print(f"Папка {pagename} успешно создана")
                    async with aiofiles.open(f'{path_dir_page}/{file.filename}', 'wb') as out_file:
                        content = file.file.read()
                        await out_file.write(content)
            else:
                await aiofiles.os.mkdir(path_vid)
                print("Создана папка video")
                if await aiofiles.os.path.exists(path_dir_page) == True:
                    print(f"Папка {pagename} уже доступна")
                    async with aiofiles.open(f'{path_dir_page}/{file.filename}', 'wb') as out_file:
                        content = file.file.read()
                        await out_file.write(content)
                else: 
                    await aiofiles.os.mkdir(path_dir_page)
                    print(f"Папка {pagename} успешно создана")
                    async with aiofiles.open(f'{path_dir_page}/{file.filename}', 'wb') as out_file:
                        content = file.file.read()
                        await out_file.write(content)
        elif file.content_type == 'application/pdf':
            path_dir_page = f"{path_pdf}{pagename}"
            if await aiofiles.os.path.exists(path_pdf) == True:
                print("Папка video уже доступна")
                if await aiofiles.os.path.exists(path_dir_page) == True:
                    print(f"Папка {pagename} уже доступна")
                    async with aiofiles.open(f'{path_dir_page}/{file.filename}', 'wb') as out_file:
                        content = file.file.read()
                        await out_file.write(content)
                else: 
                    await aiofiles.os.mkdir(path_dir_page)
                    print(f"Папка {pagename} успешно создана")
                    async with aiofiles.open(f'{path_dir_page}/{file.filename}', 'wb') as out_file:
                        content = file.file.read()
                        await out_file.write(content)
            else:
                await aiofiles.os.mkdir(path_pdf)
                print("Создана папка video")
                if await aiofiles.os.path.exists(path_dir_page) == True:
                    print(f"Папка {pagename} уже доступна")
                    async with aiofiles.open(f'{path_dir_page}/{file.filename}', 'wb') as out_file:
                        content = file.file.read()
                        await out_file.write(content)
                else: 
                    await aiofiles.os.mkdir(path_dir_page)
                    print(f"Папка {pagename} успешно создана")
                    async with aiofiles.open(f'{path_dir_page}/{file.filename}', 'wb') as out_file:
                        content = file.file.read()
                        await out_file.write(content)


@app.post("/UploadIcon/")
async def upload_icon(files: List[UploadFile] = File(), pagename: str = Form(), pagetype: str = Form()):
    print(files)
    print(pagename)
    print(pagetype)
    directory_vid = "video/"
    directory_pdf = "pdf/"
    directory_img = "img/"
    directory_site = "site/"
    directory_sp = "simplepage/"
    parent_dir = f"{Path.cwd()}/Front/public/"
    if pagetype == "Images":
        dir_icon = f"{parent_dir}{directory_img}{pagename}/icon"
        if await aiofiles.os.path.exists(dir_icon) == True:
            for file in files:
                async with aiofiles.open(f'{dir_icon}/{file.filename}', 'wb') as out_file:
                    content = file.file.read()
                    await out_file.write(content)
                    return {"IconSRC": f'/img/{pagename}/icon/{file.filename}'}
        else:
            await aiofiles.os.mkdir(dir_icon)
            for file in files:
                async with aiofiles.open(f'{dir_icon}/{file.filename}', 'wb') as out_file:
                    content = file.file.read()
                    await out_file.write(content)
                    return {"IconSRC": f'/img/{pagename}/icon/{file.filename}'}
    elif pagetype == "Video":
        dir_vid = f"{parent_dir}{directory_vid}"
        dir_new_icon = f"{dir_vid}{pagename}/icon"
        print(await aiofiles.os.path.exists(dir_vid))
        if await aiofiles.os.path.exists(dir_new_icon) == True:
            for file in files:
                async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                    content = file.file.read()
                    await out_file.write(content)
                    return {"IconSRC": f'/video/{pagename}/icon/{file.filename}'}
        else:
            await aiofiles.os.mkdir(dir_new_icon)
            for file in files:
                async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                    content = file.file.read()
                    await out_file.write(content)
                    return {"IconSRC": f'/video/{pagename}/icon/{file.filename}'}
    elif pagetype == "PDF":
        dir_pdf = f"{parent_dir}{directory_pdf}"
        dir_new_icon = f"{dir_pdf}{pagename}/icon"
        print(await aiofiles.os.path.exists(dir_pdf))
        if await aiofiles.os.path.exists(dir_new_icon) == True:
            for file in files:
                async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                    content = file.file.read()
                    await out_file.write(content)
                    return {"IconSRC": f'/pdf/{pagename}/icon/{file.filename}'}
        else:
            await aiofiles.os.mkdir(dir_new_icon)
            for file in files:
                async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                    content = file.file.read()
                    await out_file.write(content)
                    return {"IconSRC": f'/pdf/{pagename}/icon/{file.filename}'}
    elif pagetype == "SimplePage":
        dir_sp = f"{parent_dir}{directory_sp}"
        dir_new_icon = f"{dir_sp}{pagename}/icon"
        print(await aiofiles.os.path.exists(dir_sp))
        if await aiofiles.os.path.exists(dir_sp) == True:
            if await aiofiles.os.path.exists(f'{dir_sp}{pagename}') == True:
                print(await aiofiles.os.path.exists(dir_new_icon))
                if await aiofiles.os.path.exists(dir_new_icon) == True:
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/simplepage/{pagename}/icon/{file.filename}'}
                else:
                    await aiofiles.os.mkdir(dir_new_icon)
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/simplepage/{pagename}/icon/{file.filename}'}
            else:
                await aiofiles.os.mkdir(f'{dir_sp}{pagename}')
                if await aiofiles.os.path.exists(dir_new_icon) == True:
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/simplepage/{pagename}/icon/{file.filename}'}
                else:
                    await aiofiles.os.mkdir(dir_new_icon)
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/simplepage/{pagename}/icon/{file.filename}'}
        else:
            await aiofiles.os.mkdir(f"{parent_dir}{directory_sp}")
            if await aiofiles.os.path.exists(f'{dir_sp}{pagename}') == True:
                dir_new_icon = f"{dir_sp}{pagename}/icon"
                print(await aiofiles.os.path.exists(dir_new_icon))
                if await aiofiles.os.path.exists(dir_new_icon) == True:
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/simplepage/{pagename}/icon/{file.filename}'}
                else:
                    await aiofiles.os.mkdir(dir_new_icon)
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/simplepage/{pagename}/icon/{file.filename}'}
            else:
                await aiofiles.os.mkdir(f'{dir_sp}{pagename}')
                if await aiofiles.os.path.exists(dir_new_icon) == True:
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/simplepage/{pagename}/icon/{file.filename}'}
                else:
                    await aiofiles.os.mkdir(dir_new_icon)
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/simplepage/{pagename}/icon/{file.filename}'}
    elif pagetype == "Site":
        dir_site = f"{parent_dir}{directory_site}"
        dir_new_icon = f"{dir_site}{pagename}/icon"
        print(await aiofiles.os.path.exists(dir_site))
        if await aiofiles.os.path.exists(dir_site) == True:
            if await aiofiles.os.path.exists(f'{dir_site}{pagename}') == True:
                print(await aiofiles.os.path.exists(dir_new_icon))
                if await aiofiles.os.path.exists(dir_new_icon) == True:
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/site/{pagename}/icon/{file.filename}'}
                else:
                    await aiofiles.os.mkdir(dir_new_icon)
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/site/{pagename}/icon/{file.filename}'}
            else:
                await aiofiles.os.mkdir(f'{dir_site}{pagename}')
                if await aiofiles.os.path.exists(dir_new_icon) == True:
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/site/{pagename}/icon/{file.filename}'}
                else:
                    await aiofiles.os.mkdir(dir_new_icon)
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/site/{pagename}/icon/{file.filename}'}
        else:
            await aiofiles.os.mkdir(f"{parent_dir}{directory_site}")
            if await aiofiles.os.path.exists(f'{dir_site}{pagename}') == True:
                dir_new_icon = f"{dir_site}{pagename}/icon"
                print(await aiofiles.os.path.exists(dir_new_icon))
                if await aiofiles.os.path.exists(dir_new_icon) == True:
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/site/{pagename}/icon/{file.filename}'}
                else:
                    await aiofiles.os.mkdir(dir_new_icon)
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/site/{pagename}/icon/{file.filename}'}
            else:
                await aiofiles.os.mkdir(f'{dir_site}{pagename}')
                if await aiofiles.os.path.exists(dir_new_icon) == True:
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/site/{pagename}/icon/{file.filename}'}
                else:
                    await aiofiles.os.mkdir(dir_new_icon)
                    for file in files:
                        print(file.filename)
                        async with aiofiles.open(f'{dir_new_icon}/{file.filename}', 'wb') as out_file:
                            content = file.file.read()
                            await out_file.write(content)
                            return {"IconSRC": f'/site/{pagename}/icon/{file.filename}'}


@app.post("/delete_video/")
async def delete_video(videosrc: DeleteVideo):
    print(videosrc.videosrc)
    parent_dir = f"{Path.cwd()}/Front/public"
    path = f'{parent_dir}{videosrc.videosrc}'
    print(path)
    query = pages.update().where(pages.c.pagesrc == videosrc.videosrc).values(pagesrc='')
    await database.execute(query)
    await aiofiles.os.remove(f'{parent_dir}{videosrc.videosrc}')


@app.post("/delete_pdf/")
async def delete_pdf(pdfsrc: DeletePDF):
    print(pdfsrc.pdfsrc)
    parent_dir = f"{Path.cwd()}/Front/public"
    path = f'{parent_dir}{pdfsrc.pdfsrc}'
    print(path)
    query = pages.update().where(pages.c.pagesrc == pdfsrc.pdfsrc).values(pagesrc='')
    await database.execute(query)
    await aiofiles.os.remove(f'{parent_dir}{pdfsrc.pdfsrc}')


@app.post("/delete_images/")
async def delete_images(imgsrc: DeleteIMGs):
    print(imgsrc)
    parent_dir = f"{Path.cwd()}/Front/public"
    #path = f'{parent_dir}{pdfsrc.pdfsrc}'
    #print(path)
    query = pages.select().where(pages.c.pagename == imgsrc.pagename)
    get_page = await database.fetch_one(query)
    res = get_page.pagesrc
    #print(res.split(','))
    anchor = res.split(',')
    #print(anchor[0])
    #print(imgsrc.imgsrc)
    NewL = []
    for i in anchor:
        if not i in imgsrc.imgsrc and i not in NewL:
            NewL.append(i)
    dataL = ','.join(NewL)
    print(dataL)
    newquery = pages.update().where(pages.c.pagename == imgsrc.pagename).values(pagesrc=dataL)
    await database.execute(newquery)
    for i in imgsrc.imgsrc:
        #path = f'{parent_dir}{pdfsrc.pdfsrc}'
        await aiofiles.os.remove(f'{parent_dir}{i}')
        print(f"Файл {i} успешно удалён")
    return {"NewSRC": dataL}


@app.post("/delete_icon/")
async def delete_icon(IconData: IconData):
    print(IconData.iconsrc)
    parent_dir = f"{Path.cwd()}/Front/public"
    query = pages.update().where(pages.c.pageicon == IconData.iconsrc).values(pageicon='')
    await database.execute(query)
    await aiofiles.os.remove(f'{parent_dir}{IconData.iconsrc}')


@app.post("/delete_page/")
async def delete_icon(page: DelPage):
    print(page)
    query = pages.select().where(pages.c.pagename==page.pagename)
    get_page_name = await database.fetch_one(query)
    print(get_page_name.pagetype)
    if get_page_name.pagetype == "Video":
        parent_dir = f"{Path.cwd()}/Front/public/video/"
        newQ = pages.delete().where(pages.c.pagename==page.pagename)
        await database.execute(newQ)
        shutil.rmtree(f'{parent_dir}{page.pagename}')
    if get_page_name.pagetype == "SimplePage":
        parent_dir = f"{Path.cwd()}/Front/public/simplepage/"
        newQ = pages.delete().where(pages.c.pagename==page.pagename)
        await database.execute(newQ)
        shutil.rmtree(f'{parent_dir}{page.pagename}')
    if get_page_name.pagetype == "Images":
        parent_dir = f"{Path.cwd()}/Front/public/img/"
        newQ = pages.delete().where(pages.c.pagename==page.pagename)
        await database.execute(newQ)
        shutil.rmtree(f'{parent_dir}{page.pagename}')
    if get_page_name.pagetype == "PDF":
        parent_dir = f"{Path.cwd()}/Front/public/pdf/"
        newQ = pages.delete().where(pages.c.pagename==page.pagename)
        await database.execute(newQ)
        shutil.rmtree(f'{parent_dir}{page.pagename}')


if __name__ == "__main__":
    uvicorn.run("server:app", host='0.0.0.0', port=1337, reload=True)