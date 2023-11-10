<template>
  <div class="flex bg-slate-700 w-full h-screen pb-[40px]">
    <UILoading :NewVal="Load_Page" />
    <UINavmenu v-on:SetData="updateSRC"/>
    <IframesCPiframe :sendSRC="NewSRC"/>
  </div>
</template>

<script>
import axios from 'axios';
    export default {
        data() {
          return {
            DataUser: '',
            NewSRC: '/iframe/all_pages',
            Load_Page: false
          }
        },
        methods: {
          updateSRC (SuperNew) {
            this.NewSRC = SuperNew;
          }
        },
        created() {
          if (process.client) {
            if (localStorage.getItem("token")===null) {
              this.Load_Page = true;
              navigateTo("/login");
            } else {
              axios.post("http://localhost:1337/check_user", {"token": localStorage.getItem("token")})
              .then(response => {
                if (response.data.Check === 'Fail') {
                  localStorage.removeItem("token");
                  this.Load_Page = true;
                  navigateTo("/login");
                } else {
                  this.Load_Page = true;
                  this.DataUser = response.data;
                }
              })
              .catch(error => console.log(error))
            }
          }
        }
    }
</script>