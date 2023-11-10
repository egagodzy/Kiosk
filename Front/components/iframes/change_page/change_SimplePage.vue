<template>
    <div class="flex flex-col w-full">
        <form class="flex flex-col mx-auto w-full" action="">
            <input class="flex mx-5 my-5 text-center" type="text" v-model="data_for_change.pagename" placeholder="Название">
            <p class="flex mx-auto font-bold text-red-600 my-5" v-if="ErrorPageName"> {{ ErrorPageName }}</p>
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
            <input class="flex mx-5 my-5 text-center" type="text" v-model="data_for_change.pagetitle"
                placeholder="Заголовок">
            <textarea class="flex mx-5 my-5 min-h-[300px]" v-model="data_for_change.pagebody" placeholder="Текст" />
            <div class="flex mt-5 mx-auto" id="MultiSelect">
                <div id="selectBox"
                    class="flex justify-center bg-blue-500 h-10 items-center cursor-pointer hover:bg-blue-700 mx-auto text-white px-1 font-bold rounded"
                    @click.prevent="showCheckboxes">
                    Выберете страницу
                </div>
            </div>
            <div v-if="CheckBoxShow" class="flex mx-auto my-5 w-1/2 bg-white h-32 flex-col overflow-y-scroll">
                <div class="flex border hover:bg-gray-300 cursor-pointer justify-center border-black" id="CheckBox"
                    v-if="CheckBoxShow" v-for="pagename in pages" @click="GetButton(pagename.pagename)">
                    <input class="flex" type="checkbox" :id="pagename.pagename" :value="pagename.pagename"
                        v-model="checkedNames">
                    <p class="flex ml-2">{{ pagename.pagename }}</p>
                </div>
            </div>
            <div class="flex mx-auto mt-5">
                <p>Выбранные кнопки: </p>
                <div class="flex flex-wrap" v-for="NamePage in checkedNames">
                    <button @click.prevent="TestCheck(NamePage)"
                        class="bg-blue-500 hover:bg-blue-700 mx-1 text-white px-1 font-bold rounded">{{ NamePage }}</button>
                </div>
            </div>
        </form>
        <div class="flex mx-auto">
            <button class="bg-red-500 hover:bg-red-700 mx-5 text-white font-bold my-5 py-2 px-2 rounded"
                @click="GoToBack">Отмена</button>
            <button @click="ChangePage" type="submit"
                class="bg-green-500 hover:bg-green-700 mx-5 text-white font-bold my-5 py-2 px-2 rounded">Сохранить</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
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
            ErrorPageName: '',
            pages: '',
            CheckBoxShow: false,
            IconSRC: '',
            formIcon: new FormData(),
        }
    },
    created() {
        axios.get("http://localhost:1337/get_all_pages")
            .then(response => {
                this.pages = response.data;
                console.log(this.pages)
            })
            .catch(error => console.log(error));
        this.IconSRC = this.GetData.pageicon;
        if (this.GetData.pagenav) {
            let GetNav = this.GetData.pagenav.split(',');
            for (let i = 0; i < GetNav.length; i++) {
                this.checkedNames.push(GetNav[i]);
            }
        };
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
        async showCheckboxes() {
            console.log("Работает")
            if (!this.CheckBoxShow) {
                this.CheckBoxShow = true;
            } else {
                this.CheckBoxShow = false;
            }
        },
        async TestCheck(GetPageName) {
            const NewIndex = this.checkedNames.indexOf(GetPageName);
            if (NewIndex > -1) {
                this.checkedNames.splice(NewIndex, 1);
            };
            //document.getElementById(GetPageName).checked = false;
        },
        async GetButton(GetButton) {
            console.log(this.checkedNames.includes(GetButton));
            if (!this.checkedNames.includes(GetButton)) {
                this.checkedNames.push(GetButton);
                document.getElementById(GetButton).checked = true;
            } else {
                const NewIndex = this.checkedNames.indexOf(GetButton);
                if (NewIndex > -1) {
                    this.checkedNames.splice(NewIndex, 1);
                };
                document.getElementById(GetButton).checked = false;
            }
        },
        async GoToBack() {
            history.go(-1)
        },
        async ChangePage() {
            this.data_for_change.pagenav = this.checkedNames.toString()
            if (this.currentpagename === this.data_for_change.pagename) {
                this.ErrorPageName = "";
                if (this.formIcon.get('files')) {
                    this.formIcon.append('pagename', this.data_for_change.pagename);
                    this.formIcon.append('pagetype', this.data_for_change.pagetype);
                    if (this.GetData.pageicon) {
                        axios.post("http://localhost:1337/delete_icon", { "iconsrc": this.GetData.pageicon })
                            .then(response => {
                                axios.post("http://localhost:1337/UploadIcon", this.formIcon, {
                                    headers: {
                                        'Content-Type': 'multipart/form-data'
                                    }
                                })
                                    .then(response => {
                                        //console.log(response.data.IconSRC);
                                        this.data_for_change.pageicon = response.data.IconSRC;
                                        this.$emit("ChangeNewPage", this.data_for_change);
                                    })
                                    .catch(error => console.log(error))
                            })
                            .catch(error => console.log(error))
                    } else {
                        axios.post("http://localhost:1337/UploadIcon", this.formIcon, {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            }
                        })
                            .then(response => {
                                //console.log(response.data.IconSRC);
                                this.data_for_change.pageicon = response.data.IconSRC;
                                this.$emit("ChangeNewPage", this.data_for_change);
                            })
                            .catch(error => console.log(error))
                    }
                } else {
                    this.$emit("ChangeNewPage", this.data_for_change);
                }
            } else {
                axios.post("http://localhost:1337/get_pagename", { "pagename": this.data_for_change.pagename })
                    .then(response => {
                        if (response.data.status === 2) {
                            this.ErrorPageName = "Страница с таким названием существует";
                        } else {
                            this.ErrorPageName = "";
                            axios.post("http://localhost:1337/change_page_dir", { "cureent_pagename": this.currentpagename, "new_pagename": this.data_for_change.pagename })
                                .then(response => {
                                    console.log(response)
                                    if (this.formIcon.has("files")) {
                                        this.formIcon.append('pagename', this.data_for_change.pagename);
                                        this.formIcon.append('pagetype', this.data_for_change.pagetype);
                                        if (this.GetData.pageicon) {
                                            axios.post("http://localhost:1337/delete_icon", { "iconsrc": this.GetData.pageicon.replaceAll(this.currentpagename, this.data_for_change.pagename) })
                                                .then(response => {
                                                    axios.post("http://localhost:1337/UploadIcon", this.formIcon, {
                                                        headers: {
                                                            'Content-Type': 'multipart/form-data'
                                                        }
                                                    })
                                                        .then(response => {
                                                            console.log(response.data)
                                                            this.data_for_change.pageicon = response.data.IconSRC.replaceAll(this.currentpagename, this.data_for_change.pagename);
                                                            console.log("Успешно " + response.data);
                                                            this.$emit("ChangeNewPage", this.data_for_change);
                                                        })
                                                        .catch(error => console.log(error));
                                                })
                                        } else {
                                            axios.post("http://localhost:1337/UploadIcon", this.formIcon, {
                                                headers: {
                                                    'Content-Type': 'multipart/form-data'
                                                }
                                            })
                                                .then(response => {
                                                    console.log(response.data)
                                                    this.data_for_save.pageicon = response.data.IconSRC.replaceAll(this.currentpagename, this.data_for_change.pagename);
                                                    console.log("Успешно " + response.data);
                                                    this.$emit("ChangeNewPage", this.data_for_change);
                                                })
                                                .catch(error => console.log(error));
                                        }
                                        //axios.post("http://localhost:1337/UploadIcon", this.formIcon, {
                                        //    headers: {
                                        //        'Content-Type': 'multipart/form-data'
                                        //    }
                                        //})
                                        //    .then(response => {
                                        //        console.log(response.data)
                                        //        this.data_for_save.pageicon = response.data.IconSRC;
                                        //        console.log("Успешно " + response.data);
                                        //        this.$emit("ChangeNewPage", this.data_for_change);
                                        //    })
                                        //    .catch(error => console.log(error));
                                    } else {
                                        console.log("Успешно " + response.data);
                                        this.$emit("ChangeNewPage", this.data_for_change);
                                    }
                                })
                            //if (this.formIcon.has("files")) {
                            //    this.formIcon.append('pagename', this.data_for_change.pagename);
                            //    this.formIcon.append('pagetype', this.data_for_change.pagetype);
                            //    axios.post("http://localhost:1337/UploadIcon", this.formIcon, {
                            //        headers: {
                            //            'Content-Type': 'multipart/form-data'
                            //        }
                            //    })
                            //        .then(response => {
                            //            console.log(response.data)
                            //            this.data_for_save.pageicon = response.data.IconSRC;
                            //            console.log("Успешно " + response.data);
                            //            this.$emit("ChangeNewPage", this.data_for_change);
                            //        })
                            //        .catch(error => console.log(error));
                            //} else {
                            //    console.log("Успешно " + response.data);
                            //    this.$emit("ChangeNewPage", this.data_for_change);
                            //}
                        }
                    })
            }
        }
    }
}
</script>