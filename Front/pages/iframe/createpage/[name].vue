<template>
    <div class="flex w-full min-h-screen bg-blue-500">
        <div class="flex flex-col w-5/6 mx-auto my-auto bg-orange-500">
            <IframesCreatePageCreateSimplePage v-if="data_page.type_page === 'SimplePage'" v-on:CreateNewPage="CreatePage"
                :GetData='data_page' />
            <IframesCreatePageCreateVideoPage v-if="data_page.type_page === 'Video'" v-on:CreateNewPage="CreatePage"
                :GetData='data_page' />
            <IframesCreatePageCreateImagesPage v-if="data_page.type_page === 'Images'" v-on:CreateNewPage="CreatePage"
                :GetData='data_page' />
            <IframesCreatePageCreatePDFPage v-if="data_page.type_page === 'PDF'" v-on:CreateNewPage="CreatePage"
                :GetData='data_page' />
            <IframesCreatePageCreateSitePage v-if="data_page.type_page === 'Site'" v-on:CreateNewPage="CreatePage"
                :GetData='data_page' />
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            data_page: {
                type_page: '',
                name_page: '',
            },
            data_page_for_save: '',
        }
    },
    created() {
        this.data_page.name_page = this.$route.params.name;
        this.data_page.type_page = this.$route.query.TypePage;
        console.log(this.data_page)
    },
    methods: {
        async GoToBack() {
            history.go(-1)
        },
        CreatePage(NewData) {
            this.data_page_for_save = NewData;
            console.log(this.data_page_for_save);
            axios.post("http://localhost:1337/create_page/", this.data_page_for_save)
                .then(response => {
                    console.log(response.data);
                    history.go(-1);
                })
                .catch(error => console.log(error))
        }
    }
}
</script>