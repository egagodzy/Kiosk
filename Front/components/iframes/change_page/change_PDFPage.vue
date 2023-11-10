<template>
    <div class="flex flex-col w-full pb-[40px]">
        <form class="flex flex-col mx-auto w-full" action="">
            <input class="flex mx-5 my-5 text-center" type="text" v-model="data_for_change.pagename" placeholder="Название">
            <p class="flex mx-auto font-bold text-red-600 my-5" v-if="ErrorPageName">{{ ErrorPageName }}</p>
            <div class="flex">
                <svg class="flex ml-5 w-[100px] h-[100px]" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g id="page-break" transform="translate(-2 -2)"> <path id="secondary" fill="#2ca9bc" d="M5,8V4A1,1,0,0,1,6,3H18a1,1,0,0,1,1,1V8Zm0,8v4a1,1,0,0,0,1,1H18a1,1,0,0,0,1-1V16Z"></path> <path id="primary" d="M3,12H7m14,0H17m-6,0h2" fill="none" stroke="#000000" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path> <path id="primary-2" data-name="primary" d="M5,8V4A1,1,0,0,1,6,3H18a1,1,0,0,1,1,1V8" fill="none" stroke="#000000" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path> <path id="primary-3" data-name="primary" d="M5,16v4a1,1,0,0,0,1,1H18a1,1,0,0,0,1-1V16" fill="none" stroke="#000000" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path> </g> </g></svg>
                <input class="flex mx-5 my-auto w-full text-center" type="text" v-model="data_for_change.pageicon" placeholder="Иконка">
            </div>
            <input type="file" class="flex w-4/5 mx-auto mt-10 bg-blue-500" accept="application/pdf" @change="handleFileUploads( $event )"/>
            <p v-if="Error_Input"> {{ Error_Input }} </p>
            <div class="flex flex-col mx-auto mt-10" v-for="file in testG">
                <iframe class="flex w-1/3 mx-auto" :src="file.url" frameborder="0" ></iframe>
                <button v-if="file.url" @click.prevent="del_item(file.url)" class="flex mx-auto mt-5 bg-red-500 justify-center text-xl font-bold text-white rounded w-1/6">Удалить</button>
            </div>
            <div class="flex flex-col mx-auto mt-10">
                <div class="flex mx-auto">
                    <input class="flex ml-5" type="checkbox" id="test1" value="TestVid" v-model="checkedNames">
                    <label class="flex mr-5" for="test1">TestVid</label>
                    <input class="flex ml-5" type="checkbox" id="test2" value="TestImg" v-model="checkedNames">
                    <label class="flex mr-5" for="test2">TestImg</label>
                    <input class="flex ml-5" type="checkbox" id="test3" value="TestPDF" v-model="checkedNames">
                    <label class="flex mr-5" for="test3">TestPDF</label>
                    <input class="flex ml-5" type="checkbox" id="test4" value="TestSite" v-model="checkedNames">
                    <label class="flex mr-5" for="test4">TestSite</label>
                </div>
                <div class="flex mx-auto">
                    <p>Выбранные кнопки: {{ checkedNames }}</p>
                </div>
            </div>
        </form>
        <div class="flex mx-auto">
            <button class="bg-red-500 hover:bg-red-700 mx-5 text-white font-bold my-5 py-2 px-2 rounded" @click="GoToBack">Отмена</button>
            <button @click="ChangePage" type="submit" class="bg-green-500 hover:bg-green-700 mx-5 text-white font-bold my-5 py-2 px-2 rounded">Сохранить</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
    export default {
        props: {
            GetData: Object,
            GetFunc: Function
        },
        data() {
            return {
                data_for_change: this.GetData,
                currentpagename: this.GetData.pagename,
                checkedNames: [],
                NewFormData: '',
                formData: new FormData(),
                testG: [],
                Error_Input: '',
                ErrorPageName: '',
                NewValue: '',
                files: '',
            }
        },
        methods: {
            async GoToBack() {
                history.go(-1);
            },
            async ChangePage() {
                if (this.currentpagename === this.data_for_change.pagename) {
                    this.ErrorPageName = "";
                        this.testG.forEach((item) => {
                            if (item.url === this.data_for_change.pagesrc) {
                                history.go(-1);
                            }else {
                                if (this.NewValue) {
                                    if (!this.NewValue.includes('blob')) {
                                        axios.post("http://localhost:1337/delete_pdf", {"pdfsrc": this.NewValue})
                                        .then(response => {
                                            console.log(response.data);
                                        })
                                        .catch(error => console.log(error));
                                    }
                                    axios.post( 'http://localhost:1337/single-file', this.formData, {
                                        headers: {
                                            'Content-Type': 'multipart/form-data'
                                        }
                                    })
                                    .then(response => {
                                        //this.data_load = false;
                                        //this.text_load_button = "Загрузить"
                                        console.log("Успешно " + response.data);
                                        this.$emit("ChangeNewPage", this.data_for_change);
                                    })
                                    .catch(error => console.log(error));
                                }
                            }
                        });
                } else {
                    axios.post("http://localhost:1337/get_pagename", {"pagename": this.data_for_change.pagename})
                    .then(response => {
                        if (response.data.status === 2) {
                            this.ErrorPageName = "Страница с таким названием существует";
                        } else {
                            this.ErrorPageName = "";
                            this.testG.forEach((item) => {
                                if (item.url === this.data_for_change.pagesrc) {
                                    history.go(-1);
                                }else {
                                    if (this.NewValue) {
                                        if (!this.NewValue.includes('blob')) {
                                            axios.post("http://localhost:1337/delete_pdf", {"pdfsrc": this.NewValue})
                                            .then(response => {
                                                console.log(response.data);
                                            })
                                            .catch(error => console.log(error));
                                        }
                                        axios.post( 'http://localhost:1337/single-file', this.formData, {
                                            headers: {
                                                'Content-Type': 'multipart/form-data'
                                            }
                                        })
                                        .then(response => {
                                            //this.data_load = false;
                                            //this.text_load_button = "Загрузить"
                                            console.log("Успешно " + response.data);
                                            this.$emit("ChangeNewPage", this.data_for_change);
                                        })
                                        .catch(error => console.log(error));
                                    }
                                }
                            });
                        }
                    })
                    .catch(error => console.log(error)) 
                }
            },
            del_item(value) {
                console.log(value);
                this.data_for_change.pagesrc = '';
                this.testG.forEach((item, index) => {
                    if (item.url === value) {
                        console.log('У ' + item.url + ' индекс ' + index);
                        this.testG.splice(index, 1);
                    }
                })
                this.NewValue = value;
            },
            handleFileUploads(event){
                this.files = event.target.files;
                console.log("TestG dlinna: " + this.testG.length)
                if (this.testG.length === 1) {
                    this.testG.splice(1, 1);
                } else if(this.testG.length === 0) {
                    for( var i = 0; i < this.files.length; i++ ){
                        let file = this.files[i];
                        this.data_for_change.pagesrc = '/pdf/' + this.data_for_change.pagename + '/' + file.name;
                        console.log(file.name);
                        this.formData.append("files", file);
                        let Demo = {"name": this.files[i].name, "url": URL.createObjectURL(this.files[i])};
                        this.testG.push(Demo);
                    };
                    this.formData.append('pagename', this.data_for_change.pagename)
                }
                console.log("Itogovoya dlinna " + this.testG.length);
            },
        },
        created() {
            this.testG.push({"url": this.data_for_change.pagesrc});
        }
    }
</script>