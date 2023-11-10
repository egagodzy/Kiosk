<template>
    <div class="flex bg-blue-500 h-full w-full mt-10">
        <button class="flex bg-green-600 h-10 w-11 my-auto justify-center items-center rounded-full ml-5" @click="openmodal">+</button>
        <input class="flex w-full h-10 mx-5 my-2 text-2xl text-center" type="text">
    </div>
</template>

<script>
    export default {
        data() {
            return {
                OpenModal: ''
            }
        },
        methods: {
            openmodal() {
                this.OpenModal = true;
                this.$emit("OpenModal", this.OpenModal);
            }
        },
        props: {
            getModal: Function
        }
    }
</script>