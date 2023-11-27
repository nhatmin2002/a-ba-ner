import os
import shutil


def check_domain(path):
    list_domains = set()
    tests = os.listdir(path)
    for t in tests:
        domains = os.listdir(path + "/" + t)
        for d in domains:
            # print(d)
            list_domains.add(d)
    return sorted(list(list_domains))


def make_domain(domains, target):
    for d in domains:
        os.mkdir(target + "/" + d)
    print("make domain")


def move_to_domain(src, target):
    list_domains = os.listdir(target)
    tests = os.listdir(src)
    for t in tests:
        path_test = os.path.join(src, t)
        domains = os.listdir(path_test)
        for d in domains:
            path_domain = os.path.join(path_test, d)
            files = os.listdir(path_domain)
            # print(d)
            dest = os.path.join(target,d)
            # print(dest)
            for f in files:
                path_file = os.path.join(path_domain, f)
                # print(path_file)
                shutil.copy(path_file, dest)

            # list_domains.add(d)

    print("done")


if __name__ == '__main__':
    # src = "E:\VLSP\Evaluate\CacDoiSubmit\Annot"

    # src = "E:\VLSP\Evaluate\CacDoiSubmit\DoanXuanDung\VLSP_Bluesky_Team\Test-Data-Output1"
    # target = "E:\VLSP\Evaluate1\Tests\DoanXuanDung\Test_Data_Output1"

    # src = "E:\VLSP\Evaluate\CacDoiSubmit\DoanXuanDung\VLSP_Bluesky_Team\Test-Data-Output2"
    # target = "E:\VLSP\Evaluate1\Tests\DoanXuanDung\Test_Data_Output2"

    # src = "E:\VLSP\Evaluate\CacDoiSubmit\DoanXuanDung\VLSP_Bluesky_Team\Test-Data-Output3"
    # target = "E:\VLSP\Evaluate1\Tests\DoanXuanDung\Test_Data_Output3"


    # src = "E:\VLSP\Evaluate\CacDoiSubmit\\NgoVanVi\VCTUS_03"
    # target = "E:\VLSP\Evaluate1\Tests\\NgoVanVi\VCTUS_03"

    # src = "E:\VLSP\Evaluate\CacDoiSubmit\\NguyenVanNha\\test_ann"
    # target = "E:\VLSP\Evaluate1\Tests\\NguyenVanNha\\test_ann"

    # src = "E:\VLSP\Evaluate\CacDoiSubmit\PhamHoaiPhuThinh\submission_1\Test-Data"
    # target = "E:\VLSP\Evaluate1\Tests\PhamHoaiPhuThinh\submission_1"

    # src = "E:\VLSP\Evaluate\CacDoiSubmit\PhamHoaiPhuThinh\submission_2\Test-Data"
    # target = "E:\VLSP\Evaluate1\Tests\PhamHoaiPhuThinh\submission_2"
    #
    # src = "E:\VLSP\Evaluate\CacDoiSubmit\PhamHoaiPhuThinh\submission_3\Test-Data"
    # target = "E:\VLSP\Evaluate1\Tests\PhamHoaiPhuThinh\submission_3"

    # src = "E:\VLSP\Evaluate\CacDoiSubmit\PhamNgocDong\Submit"
    # target = "E:\VLSP\Evaluate1\Tests\PhamNgocDong\Submit"


    src = "E:\VLSP\Evaluate\CacDoiSubmit\VoBaoLinh\Test-Data"
    target = "E:\VLSP\Evaluate1\Tests\VoBaoLinh\Test-Data"

    domains = check_domain(src)
    make_domain(domains,target)
    move_to_domain(src, target)
