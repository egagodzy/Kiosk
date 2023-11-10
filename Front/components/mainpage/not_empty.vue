<template>
    <carousel v-if="getPageData.pagetype === 'Images'" :wrap-around="true" :autoplay="0">
        <slide class="h-screen bg-slate-700 text-white pb-[40px]" v-for="slide in imgs" :key="slide">
            <img class="h-full w-full" :src="slide" />
        </slide>
    </carousel>
    <video class="flex bg-black w-full h-screen pb-[40px]" controls="controls" v-if="getPageData.pagetype === 'Video'"
        :src="getPageData.pagesrc" type='video/mp4; codecs="avc1.42E01E, mp4a.40.2"' />
    <div v-if="getPageData.pagetype === 'SimplePage'" class="flex flex-col w-full min-h-screen bg-slate-700 pb-[40px]">
        <div class="flex w-full mt-5 mb-10 justify-center">
            <h3 class="flex text-3xl">{{ getPageData.pagetitle }}</h3>
        </div>
        <div class="flex w-full h-full">
            <p class="flex mx-5 text-xl whitespace-pre-line">{{ getPageData.pagebody }}</p>
        </div>
    </div>
    <iframe class="flex w-screen min-h-screen pb-[40px]" v-if="getPageData.pagetype === 'PDF'"
        :src="getPageData.pagesrc + configPDF" frameborder="0" />
</template>

<script>
export default {
    data() {
        return {
            configPDF: '#toolbar=0&navpanes=0&scrollbar=0"',
            imgs: '',
        }
    },
    props: {
        getPageData: Object
    },
    methods: {
        get_data() {
            console.log(this.getPageData)
        },
    },
    created() {
        this.imgs = this.getPageData.pagesrc.split(',')
        console.log(this.imgs)
    }
}
</script>