<template>
  <div class="assign-group">
    <el-dialog :visible.sync="visible" title="指定角色" @close="handleClose">
      <el-form ref="addUserForm" label-width="100px">
        <el-form-item label="用户名：">
          <el-input v-model="userName" readonly/>
        </el-form-item>
        <el-form-item label="姓名：">
          <el-select v-model="userGroups" multiple placeholder="请选择" style="width:100%">
            <el-option
              v-for="item in options"
              :key="item.id"
              :label="item.name"
              :value="item.id"/>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary">立即创建</el-button>
          <el-button >重置</el-button>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="handleClose">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import { getGroupList, updateUserGroups, getUserGroupList } from '@/api/group'
export default {
  name: 'AssignGroup',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    userId: {
      type: Number,
      default: 0
    },
    userName: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      visible: false,
      options: [],
      userGroups: []
    }
  },
  watch: {
    value(val) {
      if (val <= 0) return
      this.visible = val
      this.fetchGroupList()
      this.fetchUserGroups()
    }
  },
  methods: {
    handleClose() {
      this.visible = false
      this.$emit('input', false)
      setTimeout(() => {
        this.options = []
        this.userGroups = []
      }, 500)
    },
    fetchGroupList() {
      getGroupList({ page_size: 0 }).then(res => {
        this.options = res.results
      })
    },
    fetchUserGroups() {
      getUserGroupList(this.userId, { page_size: 0 }).then(res => {
        res.forEach((item) => {
          this.userGroups.push(item.id)
        })
      })
    },
    handleSubmit() {
      updateUserGroups(this.userId, { gids: this.userGroups }).then(() => {
        this.$message({
          message: `修改 ${this.userName} 用户组成功`,
          type: 'success'
        })
        this.handleClose()
      })
    }
  }
}
</script>
