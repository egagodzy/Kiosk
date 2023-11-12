<template>
    <div class="fixed z-50 flex flex-wrap bottom-80 opacity-80">
        <div :class="CustomStyle" v-for="button in buttons">
            <div @click="GoToButton(button.pagename)"
                class="flex flex-col w-full cursor-pointer bg-orange-500 mx-auto my-auto hover:bg-slate-500">
                <div class="flex w-full h-full mx-auto justify-center">{{ button.pagename }}</div>
                <img class="flex w-full h-full mx-auto" :src="button.pageicon" />
            </div>
        </div>
    </div>
    <carousel v-if="Page.pagetype === 'Images'" :wrap-around="true" :autoplay="0">
        <slide class="h-screen bg-slate-700 text-white pb-[40px]" v-for="slide in imgs" :key="slide">
            <img class="h-full w-full" :src="slide" />
        </slide>
    </carousel>
    <video class="flex bg-black w-full h-screen pb-[40px]" controls="controls" v-if="Page.pagetype === 'Video'"
        :src="Page.pagesrc" type='video/mp4; codecs="avc1.42E01E, mp4a.40.2"' />
    <div v-if="Page.pagetype === 'SimplePage'" class="flex flex-col w-full min-h-screen bg-slate-700 pb-[40px]">
        <div class="flex w-full mt-5 mb-10 justify-center">
            <h3 class="flex text-3xl">{{ Page.pagetitle }}</h3>
        </div>
        <div class="flex w-full h-full">
            <p class="flex mx-5 text-xl whitespace-pre-line">{{ Page.pagebody }}</p>
        </div>
    </div>
    <iframe class="flex w-screen min-h-screen pb-[40px]" v-if="Page.pagetype === 'PDF'" :src="Page.pagesrc + configPDF"
        frameborder="0" />
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            configPDF: '#toolbar=0&navpanes=0&scrollbar=0"',
            imgs: '',
            buttons: [],
            Page: '',
            CustomStyle: "flex flex-col mx-auto my-10 w-1/12 bg-slate-400"
        }
    },
    methods: {
        get_data() {
            console.log(this.Page)
        },
        GoToButton(value) {
            axios.post("http://localhost:1337/get_page_by_name", { "pagename": value })
                .then(response => {
                    if (response.data.Page.pagetype === 'Site') {
                        navigateTo(response.data.Page.pagesrc, { external: true })
                    } else {
                        navigateTo("/" + value)
                    }
                })
                .catch(error => console.log(error))
        }
    },
    async created() {
        console.log(this.$route.params.name);
        await axios.post("http://localhost:1337/get_page_by_name", { "pagename": this.$route.params.name })
            .then(response => {
                //console.log(response.data.Page)
                this.Page = response.data.Page;
                console.log(this.Page.pagetype)
                if (this.Page.pagetype === 'Site') {
                    navigateTo(this.Page.pagesrc, { external: true })
                } else {
                    console.log("ETOTYPE:" + this.Page.pagetype)
                    if (this.Page.pagetype === 'Video' || this.Page.pagetype === 'SimplePage') {
                        this.CustomStyle = '"flex flex-col mx-auto my-10 w-1/5 bg-slate-400"'
                    } else {
                        this.CustomStyle = '"flex flex-col mx-auto my-10 w-1/12 bg-slate-400"'
                    }
                    this.imgs = this.Page.pagesrc.split(',');
                    console.log(this.imgs);
                    console.log(this.Page.pagenav.split(','))
                    let GetNav = this.Page.pagenav.split(',')
                    for (let i = 0; i < GetNav.length; i++) {
                        //console.log(this.buttons[i])
                        axios.post("http://localhost:1337/get_page_by_name", { "pagename": GetNav[i] })
                            .then(response => {
                                this.buttons.push(response.data.Page)
                            })
                            .catch(error => console.log(error))
                    }
                }
            })
            .catch(error => console.log(error))
    }
}
</script>