hostip = "http://127.0.0.1:5000"

function eng2kor(eng){
    const defect_dict = {
        'Duct damage':{
            '부품':'덕트',
            '한글명':'덕트 손상'
        },
        'Bad connection':{
            '부품':'덕트',
            '한글명':'연결 불량'
        },
        'Bad tape':{
            '부품':'덕트',
            '한글명':'테이프 불량'
        },
        'Poor bolting':{
            '부품':'선박 배관',
            '한글명':'볼트 체결 불량'
        },
        'Pipe damage':{
            '부품':'선박 배관',
            '한글명':'파이프 손상'
        },
        'Step difference':{
            '부품':'선체',
            '한글명':'단차'
        },
        'Poor installation of reinforcement':{
            '부품':'선체',
            '한글명':'보강재 설치 불량'
        },
        'Bad binding':{
            '부품':'케이블',
            '한글명':'바인딩 불량'
        },
        'Poor installation':{
            '부품':'케이블',
            '한글명':'설치 불량'
        },
        'Cable damage':{
            '부품':'케이블',
            '한글명':'케이블 손상'
        },
        'Poor Processing':{
            '부품':'보온재',
            '한글명':'가공 불량'
        },
        'Insulation damage':{
            '부품':'보온재',
            '한글명':'보온재 손상'
        },
        'Poor connection processing':{
            '부품':'보온재',
            '한글명':'연계 처리 불량'
        },
        'Poor handling of tin':{
            '부품':'보온재',
            '한글명':'함석 처리 불량'
        },
    }

    return defect_dict[eng]['한글명']
}