#include <QCoreApplication>
#include <QDebug>
#include <QObject>
#include <QString>
#include <QTimer>

class Greeter : public QObject
{
    Q_OBJECT
public:
    Greeter(const QString& name, QObject *parent = 0) 
        : QObject(parent)
        , mName(name) {}

public slots:
    void run()
    {
        qDebug() << QString("Hello %1!").arg(mName);

        emit finished();
    }

signals:
    void finished();
    
private:
    const QString& mName;
};

int main(int argc, char *argv[]){
    QCoreApplication app(argc, argv);
    QCoreApplication::setApplicationName("Application Example");
    QCoreApplication::setApplicationVersion("1.0.0");

    QString name = argc > 0 ? argv[1] : "";
    if (name.isEmpty()) {
        name = "World";
    }

    Greeter* greeter = new Greeter(name, &app);
    QObject::connect(greeter, SIGNAL(finished()), &app, SLOT(quit()));
    QTimer::singleShot(0, greeter, SLOT(run()));

    return app.exec();
}

#include "main.moc"
