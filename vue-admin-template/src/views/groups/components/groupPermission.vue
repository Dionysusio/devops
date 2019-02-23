<template>
  <div class="group-permission">
    <el-dialog :visible.sync="visible" :title="title" @close="handleClose">
      <el-transfer
        v-model="groupPermission"
        :titles="transferTitle"
        :data="data"
        filterable />
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose">取 消</el-button>
        <el-button type="primary" @click="handleUpdateGroupPermission">提交修改</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import { getPermissionList, updateGroupPermissionList, getGroupPermissionList } from '@/api/permission'
export default {
  name: 'GroupPermission',
  props: {
    value: { // :value=groupPermission,@input="groupPermission = arguments[0]"
      type: Boolean,
      default: false
    },
    gid: {
      type: Number,
      default: 0
    },
    gname: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      visible: false,
      data: [],
      groupPermission: []
    }
  },
  computed: {
    title() {
      return `修改 ${this.gname} 的权限`
    },
    transferTitle() {
      return ['权限点', `${this.gname} 的权限`]
    }
  },
  watch: {
    value(val) {
      if (val === false) return
      this.visible = val
      this.fetchPermissionList() // 组件加载的时候获取权限
      this.fetchGroupPermissionList()
    }
  },
  methods: {
    handleClose() {
      this.visible = false
      this.$emit('input', false)
      setTimeout(() => {
        this.groupPermission = []
      }, 500)
    },
    fetchPermissionList() { // 获取权限列表,page_size:0 不分页
      getPermissionList({ page_size: 0 }).then(res => {
        // console.log(res)
        this.data = res.results
      })
    },
    handleUpdateGroupPermission() {
      updateGroupPermissionList(this.gid, { pids: this.groupPermission }).then(res => {
        if (res.status === 0) {
          this.$message({
            message: `修改 ${this.gname} 组的权限成功`,
            type: 'success'
          })
          this.handleClose()
        }
      })
    },
    fetchGroupPermissionList() {
      getGroupPermissionList(this.gid).then(res => {
        res.forEach((item) => {
          this.groupPermission.push(item.key)
        })
      })
    }
  }
}
</script>
<style>
  .el-transfer-panel{width:40%}
</style>
