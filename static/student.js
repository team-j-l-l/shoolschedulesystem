async function renderList() {
    let response = await fetch(`/api/student/info`);
    if (!response.ok) {
        console.error(response);
        return;
    }

    let data = await response.json();

    let tbodyEl = document.createElement("tbody");
    for (let item of data) {
        let trEl = document.createElement("tr");
        tbodyEl.append(trEl);

        let tdEl;
        tdEl = document.createElement("td");
        tdEl.innerText = item.stu_sno;
        tdEl.className = "col-stu_sno";
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "col-stu_sname";
        tdEl.innerText = item.stu_sname;
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "col-stu_sgender";
        tdEl.innerText = item.stu_sgender;
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "col-stu_sage";
        tdEl.innerText = item.stu_sage;
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "col-stu_enrolled";
        tdEl.innerText = item.stu_enrolled;
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "col-stu_major";
        tdEl.innerText = item.stu_major;
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "";
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "ctrlbar";
        tdEl.append(renderRecordCtrlbar(item));
        trEl.append(tdEl);
    }

    let tableEl = document.querySelector("#student-table");
    document.querySelector("#student-table > tbody").remove();
    tableEl.append(tbodyEl);
}

function renderRecordCtrlbar(item) {
    let ctrlbarEl = document.createElement("div");

    let editBtn = document.createElement("a");
    editBtn.className = "btn";
    editBtn.innerText = "修改";
    editBtn.onclick = (e) => {
        openEditDialog(item);
    };
    ctrlbarEl.append(editBtn);

    let delBtn = document.createElement("a");
    delBtn.className = "btn";
    delBtn.innerText = "删除";
    delBtn.onclick = (e) => {
        openComfirmationDialog({
            message: `确定要删除“${item.stu_sname}(#${item.stu_sno})”的信息？`,
            onOk: () => {
                (async () => {
                    let response = await fetch(`/api/student/${item.stu_sn}`, {
                        method: "DELETE",
                    });

                    if (!response.ok) {
                        console.error(response);
                    }

                    renderList();
                })();
            },
        });
    };
    ctrlbarEl.append(delBtn);

    return ctrlbarEl;
}

async function openEditDialog(item) {
    let dialog = document.querySelector(".student-editor");

    let dialogTitle = dialog.querySelector(".dialog-head");
    let form = dialog.querySelector("form");

    if (item) {
        dialogTitle.innerText = `修改学生信息 (#${item.stu_sn})`;
        form.elements.stu_sn.value = item.stu_sn ?? null;
        form.elements.stu_sno.value = item.stu_sno ?? "";
        form.elements.stu_sname.value = item.stu_sname ?? "";
        form.elements.stu_sgender.value = item.stu_sgender ?? "";
        form.elements.stu_sage.value = item.stu_sage ?? "";
        form.elements.stu_enrolled.value = item.stu_enrolled ?? "";
        form.elements.stu_major = item.stu_major ?? "";
    } else {
        dialogTitle.innerText = "新建学生信息";
        form.elements.stu_sn.value = null;
        form.elements.stu_sno.value = "";
        form.elements.stu_sname.value = "";
        form.elements.stu_sgender.value = "";
        form.elements.stu_sage.value = "";
        form.elements.stu_enrolled.value = "";
        form.elements.stu_major = "";
    }

    if (dialog.classList.contains("open")) {
        dialog.classList.remove("open");
    } else {
        dialog.classList.add("open");
    }
}

async function renderEditDialog() {
    let newStudentBtn = document.querySelector(".paper #new-btn");
    newStudentBtn.onclick = (e) => {
        openEditDialog();
    };

    let dialog = document.querySelector(".student-editor");

    let form = dialog.querySelector("form");

    let close_btn = dialog.querySelector("#close-btn");

    let closeDialog = () => {
        dialog.classList.remove("open");
    };

    close_btn.onclick = closeDialog;

    let save_btn = dialog.querySelector("#save-btn");
    save_btn.onclick = (e) => {
        let data = {
            stu_sn: form.elements.stu_sn.value,
            stu_sno: form.elements.stu_sno.value,
            stu_sname: form.elements.stu_sname.value,
            stu_sgender: form.elements.stu_sgender.value,
            stu_sage: form.elements.stu_sage.value,
            stu_enrolled: form.elements.stu_enrolled.value,
            stu_major: form.elements.stu_major.value,
        };

        if (!data.stu_sn) {
            // 异步执行POST请求操作
            (async () => {
                let response = await fetch("/api/student", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json;charset=utf-8",
                    },
                    body: JSON.stringify(data),
                });

                if (!response.ok) {
                    console.error(response);
                    return;
                }
                closeDialog();
                renderList();
            })();
        } else {
            // 异步执行PUT请求操作
            (async () => {
                let response = await fetch(`/api/student/${data.stu_sn}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json;charset=utf-8",
                    },
                    body: JSON.stringify(data),
                });

                if (!response.ok) {
                    console.error(response);
                    return;
                }
                closeDialog();
                renderList();
            })();
        }
    };
}

async function openComfirmationDialog({ message, onOk, onCancel }) {
    let dialog = document.querySelector(".comfirmation-dialog");

    let closeDialog = () => {
        dialog.classList.remove("open");
    };

    let okBtn = dialog.querySelector("#ok-btn");
    okBtn.onclick = (e) => {
        if (typeof onOk === "function") {
            onOk();
        }

        closeDialog();
    };

    let cancelBtn = dialog.querySelector("#cancel-btn");
    cancelBtn.onclick = (e) => {
        if (typeof onCancel === "function") {
            onCancel();
        }

        closeDialog();
    };

    let messageEl = dialog.querySelector("#message");
    messageEl.innerText = message;

    dialog.classList.add("open");
}

document.addEventListener("DOMContentLoaded", (e) => {
    renderList();
    renderEditDialog();
});