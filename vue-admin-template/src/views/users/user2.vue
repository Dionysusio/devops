<template>
  <div class="app-container">
    <el-table
      :data="userList"
      style="width: 100%">
      <el-table-column
        prop="email"
        label="email" />
      <el-table-column
        prop="username"
        label="姓名" />
      <el-table-column
        prop="is_active"
        label="状态">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.is_active"
            @change="handleUserStatusChange(scope.row)"/>
          <!-- scope.row 指的是当前用户-->
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getUserList, changeUserStatus } from '@/api/user'
export default {
  data() {
    return {
      userList: [],
      total: 0
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      getUserList().then(res => {
        this.userList = res.results
        this.total = res.count
      })
    },
    handleUserStatusChange(obj) {
      changeUserStatus(obj.id, { is_active: obj.is_active })
    //  修改obj的is_active 为当前值obj.is_active
    }
  }
}
</script>
