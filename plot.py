import json
import glob
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# liblist = ["qulacs_A100", "qulacs_H100"]  # , "qiskit"]
#liblist = ["qulacs", "pennylane"]
#liblist = ["qulacs", "pennylane", "penny_kokkos"]
# liblist = ["pennylane"]
# liblegend = ["QulacsA100", "QulacsH100"]
#liblegend = ["Qulacs", "Pennylane", "PennyKokkos"]
# liblegend = ["Pennylane"]
# liblegend = ["Qulacs", "Qiskit"]

liblist = ["qulacs", "qibojit"]
liblegend = ["Qulacs", "QIBOJit"]

def load(folder_name):
    filepaths = []

    for libname in liblist:
        path = f"./benchmark/{folder_name}/{libname}/data/*.json"
        print(f"path: {path}")
        flist = glob.glob(path)
        flist = [fname.replace("\\", "/") for fname in flist]
        print(f"flist: {flist}")
        # pick latest one
        # flist.sort(key=lambda x: int(x.split("/")[-1].split("_")[0]), reverse=True)
        if len(flist) > 0:
            filepaths.append((libname, flist[0]))

    dat = defaultdict(dict)
    for filepath in filepaths:
        print(f"filepath: {filepath}")
        data = json.load(open(filepath[1]))
        # print(f"data: {data}")

        def fetch_normal(libname, dat, data):
            items = data["benchmarks"]
            for item in items:
                name = item["group"]
                nqubits = int(item["param"])
                stats = item["stats"]
                if len(name) > 4:
                    key = libname + name[4:]
                else:
                    key = libname
                # print(key)
                dat[key][nqubits] = float(stats["min"])

        fetch_normal(filepath[0], dat, data)

    # import pprint
    # pprint.pprint(dat.keys())
    # pprint.pprint(dat)
    return dat


def plot(dat):
    cmap = plt.get_cmap("tab10")
    cnt = 0
    for ind, name in enumerate(liblist):
        hit = [dname for dname in dat.keys() if dname.startswith(name)]
        if len(hit) == 0:
            continue
        cid = liblist.index(name)
        lw = 2 if name == "qulacs" else 1

        legend = liblegend[ind]
        ls = "--" if name in ["qulacs", "qiskit", "pennylane"] else "-"
        print(legend)
        # if name not in ["qulacs", "qiskit"]:
        #     fil = np.array(list(dat[name].items())).T
        #     print(fil)
        #     plt.plot(
        #         fil[0],
        #         fil[1],
        #         ".-",
        #         label=legend,
        #         c=cmap(cid),
        #         linestyle=ls,
        #         linewidth=lw,
        #     )
        # elif name in ["qulacs"]:
        fil = np.array(list(dat[name].items())).T
        print(fil)
        plt.plot(
            fil[0],
            fil[1],
            ".-",
            label=legend,
            c=cmap(cid),
            linestyle=ls,
            linewidth=lw,
        )
        # elif name in ["qiskit"]:
        #     fil = np.array(list(dat[name + "exc"].items())).T
        #     plt.plot(
        #         fil[0],
        #         fil[1],
        #         ".-",
        #         label=legend,
        #         c=cmap(cid),
        #         linestyle=ls,
        #         linewidth=lw,
        #     )
        #     fil = np.array(list(dat[name + "optexc"].items())).T
        #     plt.plot(
        #         fil[0],
        #         fil[1],
        #         ".-",
        #         label=legend + " with opt",
        #         c=cmap(cid),
        #         linestyle="-",
        #         linewidth=lw,
        #     )

        cnt += 1

    plt.yscale("log")
    plt.grid(which="major", color="black", linestyle="-", alpha=0.3)
    plt.grid(which="minor", color="black", linestyle="-", alpha=0.1)
    plt.xlabel("# of qubits", fontsize=16)
    plt.ylabel("Time [sec]", fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)


if __name__ == "__main__":
    # for folder in ["singlethread", "multithread", "gpu"]:
    #for folder in ["multithread", "gpu"]:
    for folder in ["singlethread"]:
        dat = load(folder)

        plt.figure(figsize=(12, 6))
        plot(dat)
        plt.legend(fontsize=10, bbox_to_anchor=(1.05, 1.0))
        plt.tight_layout()
        plt.savefig(f"./image/fig_compare_{folder}.pdf")
        plt.savefig(f"./image/fig_compare_{folder}.png")
        plt.clf()
