<template>
    <div class="flex flex-col">
        <form class="flex flex-col" action="">
            <input class="flex mx-5 my-5 text-center" type="text" v-model="data_for_save.pagename" placeholder="Название">
            <p class="flex mx-auto my-5 font-bold text-red-600" v-if="ErrorPageName">{{ ErrorPageName }}</p>
            <div class="flex">
                <svg v-if="!IconSRC" class="flex ml-5 w-[100px] h-[100px]" viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg" fill="#000000">
                    <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                    <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                    <g id="SVGRepo_iconCarrier">
                        <g id="page-break" transform="translate(-2 -2)">
                            <path id="secondary" fill="#2ca9bc"
                                d="M5,8V4A1,1,0,0,1,6,3H18a1,1,0,0,1,1,1V8Zm0,8v4a1,1,0,0,0,1,1H18a1,1,0,0,0,1-1V16Z">
                            </path>
                            <path id="primary" d="M3,12H7m14,0H17m-6,0h2" fill="none" stroke="#000000"
                                stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
                            <path id="primary-2" data-name="primary" d="M5,8V4A1,1,0,0,1,6,3H18a1,1,0,0,1,1,1V8" fill="none"
                                stroke="#000000" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
                            <path id="primary-3" data-name="primary" d="M5,16v4a1,1,0,0,0,1,1H18a1,1,0,0,0,1-1V16"
                                fill="none" stroke="#000000" stroke-linecap="round" stroke-linejoin="round"
                                stroke-width="2"></path>
                        </g>
                    </g>
                </svg>
                <img v-if="IconSRC" class="flex ml-5 w-[100px] h-[100px]" :src="IconSRC">
                <input @change="UploadIcon($event)" id="PageIcon" class="hidden" type="file" accept="image/jpeg, image/png">
                <button
                    class="flex justify-center my-auto ml-20 bg-blue-500 h-1/3 items-center w-1/6 hover:bg-blue-700 text-white px-1 font-bold rounded"
                    @click.prevent="NewIcon">Изменить иконку</button>
            </div>
            <input class="flex mx-5 my-5 text-center" type="text" v-model="data_for_save.pagesrc"
                placeholder="Ссылка на сайт.">
        </form>
        <div class="flex mx-auto">
            <button class="bg-red-500 hover:bg-red-700 mx-5 text-white font-bold my-5 py-2 px-2 rounded"
                @click="GoToBack">Отмена</button>
            <button type="submit" @click="CreateNewPage"
                class="bg-green-500 hover:bg-green-700 mx-5 text-white font-bold my-5 py-2 px-2 rounded">Создать</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    props: {
        GetData: Object,
        GetFunc: Function,
    },
    data() {
        return {
            data_for_save: {
                pagename: '',
                pagetype: '',
                pageicon: '',
                pagetitle: '',
                pagebody: '',
                pagenav: '',
                pagesrc: '',
            },
            checkedNames: [],
            ErrorPageName: '',
            pages: '',
            CheckBoxShow: false,
            IconSRC: '',
            formIcon: new FormData(),
        }
    },
    created() {
        this.data_for_save.pagename = this.GetData.name_page;
        this.data_for_save.pagetype = this.GetData.type_page;
        axios.get("http://localhost:1337/get_all_pages")
            .then(response => {
                this.pages = response.data;
                console.log(this.pages)
            })
            .catch(error => console.log(error));
    },
    methods: {
        async NewIcon() {
            const inp_icon = document.getElementById("PageIcon");
            inp_icon.click()
        },
        UploadIcon(event) {
            this.files = event.target.files;
            for (let i = 0; i < this.files.length; i++) {
                let file = this.files[i];
                console.log(file.name)
                //this.AllImgsSrc.push('/img/' + this.data_for_change.pagename + '/' + file.name);
                this.formIcon.append("files", file);
                this.IconSRC = URL.createObjectURL(file);
            };
        },
        async GoToBack() {
            history.go(-1)
        },
        CreateNewPage() {
            axios.post("http://localhost:1337/get_pagename", { "pagename": this.data_for_save.pagename })
                .then(response => {
                    console.log(response.data);
                    if (response.data.status === 2) {
                        this.ErrorPageName = "Страница с таким названием существует";
                    } else {
                        if (this.formIcon.has("files")) {
                            this.formIcon.append('pagename', this.data_for_save.pagename);
                            this.formIcon.append('pagetype', this.data_for_save.pagetype);
                            axios.post("http://localhost:1337/UploadIcon", this.formIcon, {
                                headers: {
                                    'Content-Type': 'multipart/form-data'
                                }
                            })
                                .then(response => {
                                    console.log(response.data)
                                    this.data_for_save.pageicon = response.data.IconSRC;
                                    console.log("Успешно " + response.data);
                                    this.$emit("CreateNewPage", this.data_for_save);
                                })
                                .catch(error => console.log(error));
                        } else {
                            console.log("Успешно " + response.data);
                            this.$emit("CreateNewPage", this.data_for_save);
                        }
                    }
                })
                .catch(error => console.log(error))
        }
    }
}
</script>