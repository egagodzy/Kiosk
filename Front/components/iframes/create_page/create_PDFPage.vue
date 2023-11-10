<template>
    <div class="flex flex-col pb-[40px]">
        <form class="flex flex-col" action="">
            <input class="flex mx-5 my-5 text-center" type="text" v-model="data_for_save.pagename" placeholder="Название">
            <p class="flex mx-auto my-5 font-bold text-red-600" v-if="ErrorPageName">{{ ErrorPageName }}</p>
            <div class="flex">
                <svg class="flex ml-5 w-[100px] h-[100px]" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g id="page-break" transform="translate(-2 -2)"> <path id="secondary" fill="#2ca9bc" d="M5,8V4A1,1,0,0,1,6,3H18a1,1,0,0,1,1,1V8Zm0,8v4a1,1,0,0,0,1,1H18a1,1,0,0,0,1-1V16Z"></path> <path id="primary" d="M3,12H7m14,0H17m-6,0h2" fill="none" stroke="#000000" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path> <path id="primary-2" data-name="primary" d="M5,8V4A1,1,0,0,1,6,3H18a1,1,0,0,1,1,1V8" fill="none" stroke="#000000" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path> <path id="primary-3" data-name="primary" d="M5,16v4a1,1,0,0,0,1,1H18a1,1,0,0,0,1-1V16" fill="none" stroke="#000000" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path> </g> </g></svg>
                <input class="flex mx-5 my-auto w-full text-center" type="text" v-model="data_for_save.pageicon" placeholder="Иконка">
            </div>
            <input type="file" class="flex w-4/5 mx-auto mt-10 bg-blue-500" accept="application/pdf" @change="handleFileUploads( $event )"/>
            <div class="flex flex-col mx-auto mt-10" v-for="file in testG">
                <iframe class="flex w-1/3 mx-auto" :src="file.url" frameborder="0" ></iframe>
                <p class="flex mx-auto mt-5">{{ file.name }}</p>
                <button @click.prevent="del_item(file.name)" class="flex mx-auto mt-5 bg-red-500 justify-center text-xl font-bold text-white rounded w-1/3">Удалить</button>
            </div>
            <div class="flex flex-col mx-auto mt-10">
                <div class="flex mx-auto">
                    <input class="flex ml-5" type="checkbox" id="test1" value="TestVid" v-model="checkedNames">
                    <label class="flex mr-5" for="jack">TestVid</label>
                    <input class="flex ml-5" type="checkbox" id="test2" value="TestImg" v-model="checkedNames">
                    <label class="flex mr-5" for="john">TestImg</label>
                    <input class="flex ml-5" type="checkbox" id="test3" value="TestPDF" v-model="checkedNames">
                    <label class="flex mr-5" for="mike">TestPDF</label>
                    <input class="flex ml-5" type="checkbox" id="test4" value="TestSite" v-model="checkedNames">
                    <label class="flex mr-5" for="mike">TestSite</label>
                </div>
                <div class="flex mx-auto mt-10">
                    <p>Выбранные кнопки: {{ checkedNames }}</p>
                </div>
            </div>
        </form>
        <div class="flex mx-auto">
            <button class="bg-red-500 hover:bg-red-700 mx-5 text-white font-bold my-5 py-2 px-2 rounded" @click="GoToBack">Отмена</button>
            <button type="submit" @click="CreateNewPage" class="bg-green-500 hover:bg-green-700 mx-5 text-white font-bold my-5 py-2 px-2 rounded">Создать</button>
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
                files: '',
                testG: [],
                NewFormData: '',
                ErrorPageName: '',
            }
        },
        created() {
            this.data_for_save.pagename = this.GetData.name_page;
            this.data_for_save.pagetype = this.GetData.type_page;
        },
        methods: {
            async GoToBack() {
                history.go(-1)
            },
            async CreateNewPage() {
                axios.post("http://localhost:1337/get_pagename", {"pagename": this.data_for_save.pagename})
                .then(response => {
                    console.log(response.data);
                    if (response.data.status === 2) {
                        this.ErrorPageName = "Страница с таким названием существует";
                    } else {
                        this.ErrorPageName = "";
                        axios.post('http://localhost:1337/single-file', this.NewFormData, {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            }
                        })
                        .then(response => {
                            //this.data_load = false;
                            //this.text_load_button = "Загрузить"
                            console.log("Успешно " + response.data);
                            this.$emit("CreateNewPage", this.data_for_save);
                        })
                        .catch(error => console.log(error));
                    }
                })
                .catch(error => console.log(error));
            },
            del_item(value) {
                console.log(value);
                console.log(this.testG);
                this.testG.forEach((item, index) => {
                    if (item.name === value) {
                        console.log('У ' + item.name + ' индекс ' + index);
                        this.testG.splice(index, 1);
                    }
                })
                console.log(this.testG);
                console.log(this.NewFormData);
                this.NewFormData = '';
                console.log(this.NewFormData);
                //console.log(this.testG.includes(value))
            },
            handleFileUploads(event){
                this.files = event.target.files;
                console.log(this.files.length);
                let formData = new FormData();
                console.log(this.testG.length);
                if (this.testG.length <= 0) {
                    for( var i = 0; i < this.files.length; i++ ){
                        let file = this.files[i];
                        this.data_for_save.pagesrc = '/pdf/' + this.data_for_save.pagename + '/' + file.name;
                        console.log(file.name);
                        formData.append("files", file);
                        let Demo = {"name": this.files[i].name, "url": URL.createObjectURL(this.files[i])};
                        this.testG.push(Demo);
                    };
                    formData.append('pagename', this.data_for_save.pagename)
                    console.log(formData);
                    this.NewFormData = formData;
                    console.log(this.NewFormData);
                    console.log(this.data_for_save.pagesrc);
                } else {
                    this.testG.splice(2, 1);
                }
                console.log("Itogovoya dlinna " + this.testG.length);
            },
        }
    }
</script>