<template>
    <div class="flex flex-col bg-orange-600 w-1/5 h-screen">
      <button id="TestButton2" @click="DataFChild('/iframe/all_pages')" class="bg-blue-500 hover:bg-blue-700 focus:bg-blue-700 text-white font-bold mx-auto my-auto py-2 px-2 rounded">Страницы</button>
      <button id="TestButton3" @click="DataFChild('/iframe/checks')" class="bg-blue-500 hover:bg-blue-700 focus:bg-blue-700 text-white font-bold mx-auto my-auto py-2 px-2 rounded">Чеки</button>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                NewSRC: ''
            }
        },
        methods: {
            DataFChild(value) {
                this.NewSRC = value;
                this.$emit("SetData", this.NewSRC);
            }
        },
        props: {
            getSRC: Function
        }
    }
</script>