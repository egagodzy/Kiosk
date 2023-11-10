<template>
    <div class="flex flex-col w-full pb-[40px]">
        <form class="flex flex-col mx-auto w-full" action="">
            <input class="flex mx-5 my-5 text-center" type="text" v-model="data_for_change.pagename" placeholder="Название">
            <p class="flex mx-auto font-bold text-red-600 my-5" v-if="ErrorPageName">{{ ErrorPageName }}</p>
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
            <input type="file" accept="video/mp4" class="flex w-4/5 mx-auto mt-10 bg-blue-500"
                @change="handleFileUploads($event)" />
            <p v-if="Error_Input"> {{ Error_Input }} </p>
            <div class="flex flex-col mx-auto mt-10" v-for="file in testG">
                <video v-if="file.url" class="flex w-1/3 mx-auto" :src="file.url" controls="controls"
                    type='video/mp4; codecs="avc1.42E01E, mp4a.40.2"'></video>
                <button v-if="file.url" @click.prevent="del_item(file.url)"
                    class="flex mx-auto mt-5 bg-red-500 justify-center text-xl font-bold text-white rounded w-1/6">Удалить</button>
            </div>
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
            testG: [],
            Error_Input: '',
            ErrorPageName: '',
            NewValue: '',
            formData: new FormData(),
            files: '',
            IconSRC: '',
            formIcon: new FormData(),
            CheckBoxShow: false,
            pages: '',
        }
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
            history.go(-1);
        },
        async ChangePage() {
            this.data_for_change.pagenav = this.checkedNames.toString()
            if (this.currentpagename === this.data_for_change.pagename) {
                this.ErrorPageName = "";
                if (this.testG.length === 0) {
                    this.ErrorPageName = "Добавьте видео.";
                } else {
                    this.testG.forEach((item) => {
                        if (item.url === this.data_for_change.pagesrc) {
                            console.log(this.NewValue)
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
                            if (this.NewValue) {
                                this.ErrorPageName = "";
                                if (!this.NewValue.includes('blob')) {
                                    axios.post("http://localhost:1337/delete_video", { "videosrc": this.NewValue })
                                        .then(response => {
                                            console.log(response.data);
                                        })
                                        .catch(error => console.log(error));
                                }
                                axios.post('http://localhost:1337/single-file', this.formData, {
                                    headers: {
                                        'Content-Type': 'multipart/form-data'
                                    }
                                })
                                    .then(response => {
                                        //this.data_load = false;
                                        //this.text_load_button = "Загрузить"
                                        //console.log("Успешно " + response.data);
                                        //this.$emit("ChangeNewPage", this.data_for_change);
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
                                    })
                                    .catch(error => console.log(error));
                            }
                        }
                    });
                }
            } else {
                axios.post("http://localhost:1337/get_pagename", { "pagename": this.data_for_change.pagename })
                    .then(response => {
                        if (response.data.status === 2) {
                            this.ErrorPageName = "Страница с таким названием существует";
                        } else {
                            this.ErrorPageName = "";
                            if (this.testG.length === 0) {
                                this.ErrorPageName = "Добавьте видео.";
                            } else {
                                this.testG.forEach((item) => {
                                    if (item.url === this.data_for_change.pagesrc) {
                                        console.log(this.NewValue)
                                        axios.post("http://localhost:1337/change_page_dir", { "cureent_pagename": this.currentpagename, "new_pagename": this.data_for_change.pagename })
                                            .then(response => {
                                                //console.log(response.data.ChangedSRC);
                                                //this.data_for_change.pageicon = response.data.ChangedIconSRC;
                                                let CHSRC = response.data.ChangedSRC;
                                                if (this.formIcon.get('files')) {
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
                                                                        //console.log(response.data.IconSRC);
                                                                        this.data_for_change.pagesrc = CHSRC;
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
                                                                this.data_for_change.pagesrc = CHSRC;
                                                                this.data_for_change.pageicon = response.data.IconSRC;
                                                                this.$emit("ChangeNewPage", this.data_for_change);
                                                            })
                                                            .catch(error => console.log(error))
                                                    }
                                                } else {
                                                    this.data_for_change.pagesrc = response.data.ChangedSRC;
                                                    this.$emit("ChangeNewPage", this.data_for_change);
                                                }
                                            })
                                            .catch(error => console.log(error))
                                    } else {
                                        if (this.NewValue) {
                                            this.ErrorPageName = "";
                                            //console.log(this.data_for_change.pagesrc)
                                            //this.data_load = false;
                                            //this.text_load_button = "Загрузить"
                                            //console.log("Успешно " + response.data);
                                            //this.$emit("ChangeNewPage", this.data_for_change);
                                            console.log(item.name)
                                            axios.post("http://localhost:1337/change_page_dir", { "cureent_pagename": this.currentpagename, "new_pagename": this.data_for_change.pagename })
                                                .then(response => {
                                                    console.log("ETORESPONSE: " + response.data);
                                                    let CHSRC = response.data.ChangedSRC;
                                                    //this.data_for_change.pageicon = response.data.ChangedIconSRC;
                                                    if (this.formIcon.get('files')) {
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
                                                                            this.data_for_change.pageicon = response.data.IconSRC;
                                                                            //console.log(response.data.IconSRC);
                                                                            if (!this.NewValue.includes('blob')) {
                                                                                axios.post("http://localhost:1337/delete_video", { "videosrc": this.NewValue.replaceAll(this.currentpagename, this.data_for_change.pagename) })
                                                                                    .then(response => {
                                                                                        console.log(response.data);
                                                                                    })
                                                                                    .catch(error => console.log(error));
                                                                            }
                                                                            axios.post('http://localhost:1337/single-file', this.formData, {
                                                                                headers: {
                                                                                    'Content-Type': 'multipart/form-data'
                                                                                }
                                                                            })
                                                                                .then(response => {
                                                                                    this.$emit("ChangeNewPage", this.data_for_change);
                                                                                })
                                                                                .catch(error => console.log(error))
                                                                            //this.data_for_change.pagesrc = CHSRC
                                                                            //this.data_for_change.pageicon = response.data.IconSRC;
                                                                            //this.$emit("ChangeNewPage", this.data_for_change);
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
                                                                    //this.data_for_change.pagesrc = CHSRC
                                                                    this.data_for_change.pageicon = response.data.IconSRC;
                                                                    if (!this.NewValue.includes('blob')) {
                                                                        axios.post("http://localhost:1337/delete_video", { "videosrc": this.NewValue.replaceAll(this.currentpagename, this.data_for_change.pagename) })
                                                                            .then(response => {
                                                                                console.log(response.data);
                                                                            })
                                                                            .catch(error => console.log(error));
                                                                    }
                                                                    axios.post('http://localhost:1337/single-file', this.formData, {
                                                                        headers: {
                                                                            'Content-Type': 'multipart/form-data'
                                                                        }
                                                                    })
                                                                        .then(response => {
                                                                            this.$emit("ChangeNewPage", this.data_for_change);
                                                                        })
                                                                        .catch(error => console.log(error))
                                                                })
                                                                .catch(error => console.log(error))
                                                        }
                                                    } else {
                                                        if (!this.NewValue.includes('blob')) {
                                                            axios.post("http://localhost:1337/delete_video", { "videosrc": this.NewValue.replaceAll(this.currentpagename, this.data_for_change.pagename) })
                                                                .then(response => {
                                                                    console.log(response.data);
                                                                })
                                                                .catch(error => console.log(error));
                                                        }
                                                        axios.post('http://localhost:1337/single-file', this.formData, {
                                                            headers: {
                                                                'Content-Type': 'multipart/form-data'
                                                            }
                                                        })
                                                            .then(response => {
                                                                this.$emit("ChangeNewPage", this.data_for_change);
                                                            })
                                                            .catch(error => console.log(error))
                                                        //this.data_for_change.pagesrc = "/video/" + this.data_for_change.pagename + "/" + item.name;
                                                        //this.$emit("ChangeNewPage", this.data_for_change);
                                                    }
                                                })
                                                .catch(error => console.log(error));
                                        }
                                    }
                                });
                            }
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
        handleFileUploads(event) {
            this.files = event.target.files;
            console.log("TestG dlinna: " + this.testG.length)
            if (this.testG.length === 1) {
                this.testG.splice(1, 1);
            } else if (this.testG.length === 0) {
                for (var i = 0; i < this.files.length; i++) {
                    let file = this.files[i];
                    this.data_for_change.pagesrc = '/video/' + this.data_for_change.pagename + '/' + file.name;
                    console.log(file.name);
                    this.formData.append("files", file);
                    let Demo = { "name": this.files[i].name, "url": URL.createObjectURL(this.files[i]) };
                    this.testG.push(Demo);
                };
                this.formData.append('pagename', this.data_for_change.pagename)
            }
            console.log("Itogovoya dlinna " + this.testG.length);
        },
    },
    created() {
        this.testG.push({ "url": this.data_for_change.pagesrc });
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
    }
}
</script>