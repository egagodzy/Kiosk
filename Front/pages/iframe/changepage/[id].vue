<template>
    <div class="flex w-full min-h-screen bg-orange-500">
        <IframesChangePageChangeSimplePage v-if="data_for_change.pagetype === 'SimplePage'" v-on:ChangeNewPage="changePage" :GetData="data_for_change" />
        <IframesChangePageChangeVideoPage v-if="data_for_change.pagetype === 'Video'" v-on:ChangeNewPage="changePage" :GetData="data_for_change" />
        <IframesChangePageChangePDFPage v-if="data_for_change.pagetype === 'PDF'" v-on:ChangeNewPage="changePage" :GetData="data_for_change" />
        <IframesChangePageChangeImagesPage v-if="data_for_change.pagetype === 'Images'" v-on:ChangeNewPage="changePage" :GetData="data_for_change" />
    </div>
</template>

<script>
import axios from 'axios';
    export default {
        data() {
            return {
                data_for_change: {
                    pagename: '',
                    pagetype: '',
                    pageicon: '',
                    pagetitle: '',
                    pagebody: '',
                    pagenav: '',
                    pagesrc: ''
                },
                checkedNames: [],
            }
        },
        created() {
            axios.post("http://localhost:1337/get_page_by_id", {"id": this.$route.params.id})
            .then(response => {
                let TestPage = response.data.Page;
                this.data_for_change.pagename = TestPage.pagename;
                this.data_for_change.pagetype = TestPage.pagetype;
                this.data_for_change.pageicon = TestPage.pageicon;
                this.data_for_change.pagetitle = TestPage.pagetitle;
                this.data_for_change.pagebody = TestPage.pagebody;
                this.data_for_change.pagenav = TestPage.pagenav;
                this.data_for_change.pagesrc = TestPage.pagesrc;
            })
            .catch(error => console.log(error))
        },
        methods: {
            async GoToBack() {
                history.go(-1)
            },
            changePage(NewDataFile) {
                NewDataFile.pageid = this.$route.params.id;
                axios.post("http://localhost:1337/change_page/", NewDataFile)
                .then(response => {
                    console.log(response.data);
                    history.go(-1);
                })
                .catch(error => console.log(error))
            }
        }
    }
</script>