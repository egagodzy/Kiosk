<template>
    <div class="flex border-2 border-orange-500 rounded mx-10 my-10 bg-indigo-600">
        <table class="flex flex-col w-full h-full">
            <thead>
                <tr class="flex w-full text-2xl bg-orange-600">
                    <th class="flex justify-center w-full mx-auto">ID</th>
                    <th class="flex justify-center w-full mx-auto">Название</th>
                    <th class="flex justify-center w-full mx-auto">Тип</th>
                    <th class="flex justify-center w-full mx-auto">Удалить</th>
                </tr>
            </thead>
            <tbody>
                <tr class="flex text-2xl my-2 hover:bg-indigo-700" v-for="page in pageList">
                    <td class="flex justify-center items-center cursor-pointer border-2 border-orange-600 w-full"
                        @click="TestTake(page)">{{ page.id }}</td>
                    <td class="flex justify-center items-center cursor-pointer border-2 border-orange-600 w-full"
                        @click="TestTake(page)">{{ page.pagename }}</td>
                    <td class="flex justify-center items-center cursor-pointer border-2 border-orange-600 w-full"
                        @click="TestTake(page)">{{ page.pagetype }}</td>
                    <td class="flex justify-center border-2 border-orange-600 w-full h-full">
                        <button @click="DelPage(page.pagename)"
                            class="flex cursor-pointer bg-red-500 hover:bg-red-700 text-white w-full h-4/5 justify-center my-2 mx-2 rounded-lg">Удалить</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    props: {
        pageList: Array
    },
    methods: {
        TestTake(page) {
            navigateTo("/iframe/changepage/" + page.id);
        },
        DelPage(value) {
            console.log(value)
            axios.post("http://localhost:1337/delete_page/", { "pagename": value })
                .then(response => {
                    console.log(response);
                    location.reload();
                })
                .catch(error => console.log(error))
        }
    }
}
</script>