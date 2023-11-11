<template>
    <div v-if="testModal === true" class="fixed flex min-h-screen w-full bg-slate-700">
        <div class="flex flex-col mx-auto my-auto w-5/6">
            <input class="flex mt-10 mx-10 text-center" v-model="TestPage" type="text"
                placeholder="Введите название страницы">
            <p class="mx-auto text-red-600" v-if="Error_NamePage"> {{ Error_NamePage }}</p>
            <div class="flex flex-col my-10">
                <div class="flex mx-auto w-full">
                    <p class="mx-auto"><input class="mr-1" v-model="rad_pick" name="TypePage" type="radio"
                            value="SimplePage"> Обычная страница</p>
                    <p class="mx-auto"><input class="mr-1" v-model="rad_pick" name="TypePage" type="radio"
                            value="Video">Видео</p>
                    <p class="mx-auto"><input class="mr-1" v-model="rad_pick" name="TypePage" type="radio"
                            value="Images">Изоображения</p>
                    <p class="mx-auto"><input class="mr-1" v-model="rad_pick" name="TypePage" type="radio" value="PDF">PDF
                    </p>
                    <p class="mx-auto"><input class="mr-1" v-model="rad_pick" name="TypePage" type="radio" value="Site">Сайт
                    </p>
                </div>
                <div class="flex mx-auto">
                    <h1 class="mx-auto text-red-600" v-if="Error_RadioPick">{{ Error_RadioPick }}</h1>
                </div>
            </div>
            <div class="flex w-full mx-auto mb-10">
                <button class="bg-green-500 hover:bg-green-700 text-white font-bold mx-auto my-auto py-2 px-2 rounded"
                    @click="TestGoTo">Переход</button>
                <button class="bg-red-500 hover:bg-red-700 text-white font-bold mx-auto my-auto py-2 px-2 rounded"
                    @click="CloseModal">Отмена</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            ModalOpen: '',
            TestPage: '',
            rad_pick: '',
            Error_NamePage: '',
            Error_RadioPick: '',
        }
    },
    methods: {
        CloseModal() {
            this.ModalOpen = false;
            this.$emit("CloseModal", this.ModalOpen);
        },
        async TestGoTo() {
            console.log(this.rad_pick);
            if (this.TestPage === '') {
                this.Error_NamePage = "";
                this.Error_RadioPick = "";
                this.Error_NamePage = "Поле название страницы не может быть пустым.";
            } else if (this.rad_pick === '') {
                console.log("Работает")
                this.Error_NamePage = "";
                this.Error_RadioPick = "";
                this.Error_RadioPick = "Выберете тип страницы."
            } else {
                axios.post("http://localhost:1337/get_pagename", { "pagename": this.TestPage })
                    .then(response => {
                        if (response.data.status === 2) {
                            this.Error_NamePage = "Страница с таким названием существует";
                        } else {
                            this.Error_NamePage = "";
                            navigateTo("/iframe/createpage/" + this.TestPage + "?TypePage=" + this.rad_pick)
                        }
                    })
            }
        }
    },
    props: {
        getModalShow: Function,
        testModal: Boolean
    }
}
</script>